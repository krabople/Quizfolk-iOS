import sys,pathlib,json,time
r=pathlib.Path(__file__).resolve().parents[1]
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--source-bank',type=pathlib.Path,required=True);parser.add_argument('--work',type=pathlib.Path,required=True);args=parser.parse_args();work=args.work;sys.path.insert(0,str(work/'audit-libs'))
import numpy as np,onnxruntime as ort
from tokenizers import Tokenizer
p=work/'audit-model';tok=Tokenizer.from_file(str(p/'tokenizer.json'));tok.enable_truncation(max_length=128);tok.enable_padding()
opts=ort.SessionOptions();opts.intra_op_num_threads=4;opts.inter_op_num_threads=1
sess=ort.InferenceSession(str(p/'model_quantized.onnx'),sess_options=opts,providers=['CPUExecutionProvider'])
print('Model inputs',[(x.name,x.shape) for x in sess.get_inputs()],flush=True)
q=json.loads(args.source_bank.read_text(encoding='utf-8'))
texts=[x['prompt']+' Answers: '+'; '.join(x['answers']) for x in q]
out=[];start=time.time()
for i in range(0,len(texts),64):
 enc=tok.encode_batch(texts[i:i+64]);ids=np.array([x.ids for x in enc],dtype=np.int64);mask=np.array([x.attention_mask for x in enc],dtype=np.int64)
 inputs={'input_ids':ids,'attention_mask':mask}
 if any(x.name=='token_type_ids' for x in sess.get_inputs()):inputs['token_type_ids']=np.zeros_like(ids)
 hidden=sess.run(None,inputs)[0];v=(hidden*mask[:,:,None]).sum(1)/np.maximum(mask.sum(1)[:,None],1);v/=np.maximum(np.linalg.norm(v,axis=1,keepdims=True),1e-12);out.append(v.astype('float32'))
 if i%1024==0:print(i,'/',len(q),'seconds',round(time.time()-start),flush=True)
np.save(work/'question-embeddings.npy',np.concatenate(out));print('Complete',round(time.time()-start),flush=True)
