<?php
declare(strict_types=1);

// Formatting differences and separate source IDs do not make a new question.
// Fold case, quote typography, repeated spacing and terminal prose punctuation.
// Preserve internal punctuation, word boundaries and numerical notation: 1.2,
// 12, 6!, 6, 2-3 and 23 are different questions. This is not paraphrase detection.
function question_prompt_key(string $prompt):string {
    static $fold=null;
    $fold ??= json_decode(file_get_contents(__DIR__.'/name-fold.json'),true,512,JSON_THROW_ON_ERROR);
    if(class_exists('Normalizer'))$prompt=Normalizer::normalize($prompt,Normalizer::FORM_KC) ?: $prompt;
    $prompt=strtr(strtr($prompt,$fold),['‘'=>"'",'’'=>"'",'“'=>'"','”'=>'"']);
    $prompt=trim(preg_replace('/[\p{Z}\p{C}\s]+/u',' ',$prompt) ?? '');
    $prompt=preg_replace('/\?+$/u','',$prompt) ?? '';
    return preg_replace('/(?<=\p{L})[.!]+$/u','',$prompt) ?? '';
}
function unique_questions(array $questions):array {
    $ids=[];$prompts=[];$unique=[];
    foreach($questions as $q) {
        $key=question_prompt_key($q['prompt']);
        if($key==='' || isset($ids[$q['id']]) || isset($prompts[$key]))continue;
        $ids[$q['id']]=true;$prompts[$key]=true;$unique[]=$q;
    }
    return $unique;
}
function question_deck(array $bank,array $seenIDs=[]):array {
    $seenPrompts=[];
    foreach($bank as $q)if(isset($seenIDs[$q['id']]))$seenPrompts[question_prompt_key($q['prompt'])]=true;
    $fresh=[];$repeated=[];
    foreach($bank as $q) {
        if(isset($seenIDs[$q['id']]) || isset($seenPrompts[question_prompt_key($q['prompt'])]))$repeated[]=$q;
        else $fresh[]=$q;
    }
    shuffle($fresh);shuffle($repeated);
    return unique_questions(array_merge($fresh,$repeated));
}
