"""Package only the public download page and the verified, signed Android APK."""
import hashlib
import json
from pathlib import Path
import shutil
import stat
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

repo = Path(__file__).resolve().parents[1]
workspace = repo.parent.parent
apk_name = 'Quizfolk-Android-0.3.3-11.apk'
apk = repo.parent / apk_name
report = json.loads((repo.parent / 'Quizfolk-Android-0.3.3-11-verification.json').read_text())
assert hashlib.sha256(apk.read_bytes()).hexdigest() == report['apkSHA256']
assert report['signed'] and report['fcmClientConfigured']
stage = workspace / 'work/quizfolk-download-site'
stage.mkdir(parents=True, exist_ok=True)
files = {
    'index.html': repo / 'web-download/index.html',
    '.htaccess': repo / 'web-download/.htaccess',
    'logo.png': repo / 'iOS/Assets.xcassets/AppIcon.appiconset/AppIcon.png',
    'nunito.ttf': repo / 'android/app/src/main/res/font/nunito.ttf',
    'font-license.txt': repo / 'android/FONT-LICENSE.txt',
    apk_name: apk,
}
for name, source in files.items():
    shutil.copyfile(source, stage / name)
(stage / 'SHA256SUMS.txt').write_text(report['apkSHA256'] + '  ' + apk_name + '\n')
archive = repo.parent / 'Quizfolk-Android-download-page-20261105.zip'
with ZipFile(archive, 'w', ZIP_DEFLATED) as z:
    for name in [*files, 'SHA256SUMS.txt']:
        item = ZipInfo('public_html/quizfolk-download/' + name)
        item.create_system = 3
        item.external_attr = (stat.S_IFREG | 0o644) << 16
        item.compress_type = ZIP_DEFLATED
        z.writestr(item, (stage / name).read_bytes())
print(json.dumps({'archive': str(archive), 'preview': str(stage), 'apkSHA256': report['apkSHA256'], 'files': len(files) + 1}))
