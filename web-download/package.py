"""Package only the public download page and the verified, signed Android APK."""
import hashlib
import json
from datetime import datetime
from pathlib import Path
import shutil
import stat
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

repo = Path(__file__).resolve().parents[1]
workspace = repo.parent.parent
apk_name = 'Quizfolk-Android-0.3.3-15.apk'
apk = repo.parent / apk_name
report = json.loads((repo.parent / 'Quizfolk-Android-0.3.3-15-verification.json').read_text())
assert hashlib.sha256(apk.read_bytes()).hexdigest() == report['apkSHA256']
assert report['signed'] and report['fcmClientConfigured']
stage_home = workspace / 'work/quizfolk-download-home'
stage = stage_home / 'public_html/quizfolk-download'
stage.mkdir(parents=True, exist_ok=True)
files = {
    'index.html': repo / 'web-download/index.html',
    '.htaccess': repo / 'web-download/.htaccess',
    'download.php': repo / 'web-download/download.php',
    'stats.php': repo / 'web-download/stats.php',
    'stats.js': repo / 'web-download/stats.js',
    'stats.css': repo / 'web-download/stats.css',
    'logo.png': repo / 'iOS/Assets.xcassets/AppIcon.appiconset/AppIcon.png',
    'nunito.ttf': repo / 'android/app/src/main/res/font/nunito.ttf',
    'font-license.txt': repo / 'android/FONT-LICENSE.txt',
    apk_name: apk,
}
for name, source in files.items():
    shutil.copyfile(source, stage / name)
(stage / 'SHA256SUMS.txt').write_text(report['apkSHA256'] + '  ' + apk_name + '\n')
archive = repo.parent / 'Quizfolk-Android-download-page-0.3.3-15.zip'
helper = stage_home / 'quizfolk-service/download-tracking/metrics.php'
helper.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(repo / 'web-download/server/metrics.php', helper)
with ZipFile(archive, 'w', ZIP_DEFLATED) as z:
    targets = [('public_html/quizfolk-download/' + name, stage / name) for name in [*files, 'SHA256SUMS.txt']]
    targets.append(('quizfolk-service/download-tracking/metrics.php', helper))
    for target, source in targets:
        item = ZipInfo(target, date_time=datetime.now().timetuple()[:6])
        item.create_system = 3
        item.external_attr = (stat.S_IFREG | 0o644) << 16
        item.compress_type = ZIP_DEFLATED
        z.writestr(item, source.read_bytes())
print(json.dumps({'archive': str(archive), 'preview': str(stage), 'apkSHA256': report['apkSHA256'], 'files': len(targets)}))
