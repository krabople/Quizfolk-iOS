"""Author's second, individual editorial pass; not an independent review."""
import json,pathlib
p=pathlib.Path(__file__).parent
q=json.loads((p/'draft.json').read_text(encoding='utf8'))
notes='''Space bar inserts ordinary word spaces; the three other keys do not.
Shift temporarily selects capitals, unlike the persistent Caps Lock toggle.
Backspace removes the preceding character; Delete commonly removes the following one.
Plain-text editor qualification makes Enter a newline rather than a word-processor paragraph distinction.
The insertion cursor identifies the next text position; improve distracting physical-device choices.
Selection identifies the passage affected by copying or formatting; it does not change hardware.
Undo reverses a recent edit, without guaranteeing reversal of every past action.
Cut removes the selected source text; Copy normally preserves it.
Paste inserts clipboard content, while Find, Print and Zoom have separate functions.
Find searches specified content within a document; replace physical-object distractors.
Bold conventionally gives heavier strokes; no other listed style changes stroke weight.
Italic commonly slants right; usually avoids claiming every typeface must do so.
Underline adds a line beneath characters, unlike strike-through or a border.
A font supplies character designs rather than storage or hardware.
Font size changes character size, not keyboard dimensions.
Bullets are list markers, not numbering or account prompts.
A spellchecker flags possible spelling errors; it does not establish factual truth.
A page margin is the blank region outside the main text area.
Landscape is wider than tall; a picture subject does not define orientation.
Replace the portrait question duplicated in General Knowledge with the distinct Save As function.
Print preview shows the intended printed layout, not internal printer components.
A page break puts following content on a new page, rather than merely ending a line.
Spreadsheet rows run horizontally in the ordinary grid.
Spreadsheet columns run vertically in the ordinary grid.
A cell is one row-column intersection, distinct from the whole row or sheet.
Explicit A1 notation makes A the column and 3 the row, avoiding R1C1 ambiguity.
A formula calculates using values or references; improve software-related distractors.
Replace alphabetical sorting, already in General Knowledge, with percentage display: 0.5 equals 50%.
Filtering hides nonmatching rows from the view; it does not permanently delete them.
Rectangular bars identify a bar chart, unlike the three named alternative charts.
Circle slices representing parts of one whole identify a pie chart.
A slide is one presentation page; not a physical computer component.
A transition occurs between slides, unlike an animation of an object within a slide.
Speaker notes are presenter reminders; they are not automatically intended for the audience.
An email attachment is an accompanying file, not a subject line or connection cable.
The subject line states the message topic; replace hardware distractors with real email fields.
Inbox is the normal incoming-message folder, although rules can redirect mail.
A draft is saved unsent mail, not necessarily a deleted or printed message.
Forward sends received content onward; it cannot alter the original sender identity.
Reply All addresses the original sender and the To/Cc recipients; clarify that it excludes hidden Bcc recipients.
Bcc conceals the added recipient addresses from other recipients; improve distractors without claiming it conceals the sender.
Email spam is unsolicited bulk messaging; the options do not include another accepted definition.
Contacts store people and their details, not all filesystem contents.
Muting blocks transmission of the local microphone input; it does not mute everybody else.
Screen sharing presents screen content remotely; it does not itself grant account credentials.
A webcam captures live images, not a paper scan or temperature measurement.
A microphone is an audio input; monitor, printer and projector are outputs.
A projector throws an image onto a receiving surface; the other devices do not.
A scanner digitises a paper photograph; distinguish from audio or network equipment.
A touchpad controls the on-screen pointer through finger movement.
Downloading receives data from a remote source; uploading is the opposite direction.
Uploading sends the local image to the service; improve unrelated distractors.
Hyperlinks navigate to a target, which can be another location in the same document.
A bookmark saves a reference for revisiting a page; it does not guarantee an offline copy.
Tabs contain multiple browsing pages within one window, rather than requiring separate windows.
An address bar accepts a web address, though it can also accept search terms.
Refresh requests/reloads content; it cannot guarantee that the server content has changed.
A home page is a site main/introductory page, not the owner physical address.
A search engine retrieves matches to a query; it is not limited to local printer contents.
Back normally traverses the current tab history; it does not undo webpage author edits.
Scrolling changes the portion visible in the viewport without rewriting the document.
A pop-up is an additional window; it is not a physical hinge or a tab necessarily.
Page zoom enlarges displayed content, not hardware or the stored data size.
Folders organise files and nested folders; they are not limited to a particular file type.
A subfolder is nested within another folder; replace implausible printer distractor.
The suffix .jpg is a filename extension; it is not the whole base name.
.txt conventionally denotes plain text; jpg, mp3 and mp4 are distinct media types.
.mp3 conventionally denotes audio, unlike txt, csv and jpg.
.mp4 most clearly suggests video among these options; wording deliberately avoids claiming every MP4 contains video.
Renaming changes the identifier; it does not convert the contents into a different format.
A backup supports recovery from loss/damage; it cannot guarantee no failures.
An external drive is physically outside the case; it can be a hard drive or solid-state storage.
A USB flash drive carries data between devices; it is not an optical projector.
Replace the second copying question with ZIP bundling, preserving variety and avoiding a near-repeat of Cut/Copy.
A password supplies authentication evidence; it is not storage capacity or display brightness.
Unique passwords avoid reuse. The question does not claim uniqueness alone guarantees security.
A password manager stores/manages credentials, distinct from hardware maintenance.
Two-factor authentication requires two distinct factor types, not simply two copies of one password.
Phishing uses deception to induce disclosure or unsafe action; replace absurd distractors with computing operations.
Signing out ends a session rather than deleting the account or operating system.
Locking helps protect an unattended authenticated session; replace physical-size distractors.
Ransomware demands payment after restricting access; paying is not a guarantee of recovery.
Antivirus targets malware; it does not promise every threat is detected.
Software updates commonly provide fixes/improvements; not every update necessarily adds a feature.
Read-only permits viewing but not changing the stored original; local copies do not invalidate this distinction.
A user account groups an identity, permissions and settings; it is not a hardware inventory count.
Guest access is commonly temporary/restricted; wording avoids promising identical restrictions on every operating system.
Wi-Fi joins wireless local networks; internet access is a separate service.
SSID is the advertised wireless network identifier; use related technical acronyms as distractors.
Offline here means disconnected from the online service, not a guarantee every app function stops.
A progress bar expresses completion, not necessarily remaining time or processor temperature.
A screenshot captures displayed imagery; screen recordings differ by capturing a sequence.
Cropping removes outer image areas; it does not add audio or encrypt unrelated files.
A pixel is a picture element. Avoid claiming every display uses identical physical pixel arrangements.
A thumbnail is a small preview; it need not depict a literal thumb.
Drag and drop carries an interface item with a held pointer action before release; use sensible interface alternatives.
Desktop wallpaper is the background design, not material pasted inside hardware.
An app icon represents an application; it need not reveal how many files it uses.
Minimising hides the window without quitting; it is not the same as closing or uninstalling.
A software bug is a defect; replace literal-insect and cleaning-product distractors with software concepts.'''.splitlines()
assert len(q)==len(notes)==100
MS='https://support.microsoft.com/en-us/'
sources={}
def span(a,b,url):
 for i in range(a,b+1):sources[i]=url
span(1,5,MS+'accessibility/windows/keyboard-shortcuts-in-windows')
span(6,22,MS+'word/basic-tasks-in-word')
span(23,31,MS+'excel/basic-tasks-in-excel')
span(32,34,MS+'powerpoint/training/give-a-presentation-in-powerpoint')
span(35,43,MS+'outlook/basic-tasks-in-outlook')
span(44,50,'https://support.apple.com/guide/mac-help/welcome/mac')
span(51,63,'https://support.mozilla.org/en-US/kb/how-use-firefox')
span(64,74,MS+'windows/experience/storage-filemanagement/common-file-name-extensions-in-windows')
span(75,81,'https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online/password-managers')
span(82,84,'https://www.ncsc.gov.uk/pdfs/guidance/mitigating-malware-and-ransomware-attacks.pdf')
span(85,100,'https://support.apple.com/guide/mac-help/welcome/mac')
sources.update({28:MS+'excel/format-numbers-as-percentages-in-excel',33:MS+'powerpoint/training/add-change-or-remove-transitions-between-slides',40:MS+'outlook/reply-to-or-forward-an-email-message',41:MS+'outlook/create-reply-to-or-forward-email-messages-in-outlook-on-the-web',54:'https://support.mozilla.org/en-US/kb/bookmarks-firefox',56:'https://support.mozilla.org/en-US/kb/address-bar-autocomplete-firefox',74:MS+'windows/experience/storage-filemanagement/zip-and-unzip-files',79:'https://www.ncsc.gov.uk/guidance/phishing',87:'https://support.apple.com/guide/mac-help/mh15600/mac',88:'https://support.apple.com/en-us/102766',89:'https://support.apple.com/en-us/102766'})
changes={
5:{'answers':['Where the next typed character will appear','Where the last spelling error was found','Where the document was last saved','Where the next page ends']},
6:{'answers':['Apply an action such as copying or formatting it','Automatically translate the entire document','Recover every previous version of the file','Remove all the document margins']},
10:{'answers':['Specified words or characters','An earlier version of the file','The default printer settings','The document page orientation']},
13:{'answers':['A line beneath the text','A line through the text','A box around each paragraph','A shadow behind each letter']},
15:{'answers':['Makes the text characters larger','Makes only the spaces wider','Changes lowercase letters to capitals','Changes the page background colour']},
16:{'answers':['A symbol such as a dot','A page break','A footnote containing a source','An email address']},
20:{'prompt':'Which command commonly saves a document under a different filename?','answers':['Save As','Undo','Find','Zoom'],'rationale':'Save As allows saving under a new name; Undo reverses an edit, Find searches and Zoom changes magnification.'},
27:{'answers':['Calculating a result from values or references','Setting the page orientation','Protecting the file with a password','Choosing the printer paper size']},
28:{'prompt':'A spreadsheet cell contains 0.5. What does percentage formatting normally display?','answers':['50%','0.5%','5%','500%'],'rationale':'Percentage format displays the stored decimal as a fraction of one hundred: 0.5 is 50 percent.'},
29:{'answers':['Shows rows that meet chosen conditions','Permanently deletes all duplicate rows','Sorts every column into descending order','Converts every formula into plain text']},
36:{'answers':['The subject line','The recipient address','The attachment filename','The signature']},
40:{'answers':['Addresses a reply to the sender and the recipients on the To and Cc lines','Replies only to the sender','Includes every hidden Bcc recipient automatically','Forwards the message to all saved contacts']},
41:{'answers':['Include recipients whose addresses are hidden from the other recipients','Hide the sender address from everyone','Automatically encrypt every attachment','Prevent any recipient from forwarding the message']},
45:{'answers':['Showing other participants content from your screen','Automatically sending every file on your computer','Giving every participant control of your keyboard','Changing the background behind your camera image']},
52:{'answers':['Sending the image from your device to the website','Saving a copy from the website to your device','Changing the image filename on your device only','Printing the image from your browser']},
56:{'answers':['A web address','Only a page number in a printed document','Only the name of a locally installed font','Only a spreadsheet formula']},
65:{'answers':['A folder located inside another folder','A file compressed into a smaller image','A shortcut to a printer','A program running without a window']},
74:{'prompt':'What can a ZIP archive be used to do?','answers':['Bundle several files into one archive','Translate every document into another language','Turn every photograph into a video','Increase the resolution of every image'],'rationale':'ZIP packages files in one archive and can compress them; already compressed data may not shrink appreciably.'},
77:{'answers':['Store and help manage account passwords','Check documents for spelling errors','Arrange browser tabs by colour','Remove unwanted email attachments']},
78:{'answers':['Two different types of evidence to verify a login','Two identical copies of the same password','Two different usernames with no other checks','Two browser tabs showing the same login page']},
79:{'answers':['Revealing information or taking an unsafe action through deception','Removing blank rows from a spreadsheet','Compressing files into an archive','Changing the resolution of a photograph']},
81:{'prompt':'Why should you lock a computer when leaving it unattended in a shared workspace?','answers':['To help prevent others using your signed-in session','To permanently delete your saved documents','To give other users your account permissions','To change the password of every account']},
82:{'answers':['A payment','A spelling correction','A screen-resolution change','A software licence review with no charge']},
83:{'answers':['Malicious software','Misspelled names in every document','Duplicate photographs in every folder','Unused contacts in an address book']},
84:{'answers':['Fixes or improvements to the software','A new physical computer case','A guarantee that all files are backed up','A guaranteed increase in internet contract speed']},
89:{'answers':['An SSID','A URL','A PDF','A CPU']},
91:{'answers':['How much of the operation has been completed','The current processor temperature','The age of the file owner','The number of files permanently deleted']},
93:{'answers':['Removes unwanted outer parts of the image','Adds a coloured border around the image','Rotates the whole image clockwise','Combines two images side by side']},
95:{'answers':['A small preview of a larger image or document','A full-resolution backup of every file','A list of all the image metadata','A password-protected image folder']},
96:{'answers':['Move an item while holding it with the pointer, then release it','Click an item twice without moving the pointer','Use a keyboard shortcut to close a window','Scroll a page without selecting an item']},
98:{'answers':['A program you can open','The size of a downloaded file','The number of pages in a document','The current battery charge']},
100:{'answers':['An error or defect in a program','A new feature added intentionally','A licence allowing software installation','A copy saved for data recovery']},
}
rows=[]
for i,(draft,note) in enumerate(zip(q,notes),1):
 change={'sourceURL':sources[i],**changes.get(i,{})}
 rows.append({'row':i,'prompt':draft['prompt'],'action':'edit','note':note,'meaning':True,'answerCorrect':True,'onlyOneCorrect':True,'grammar':True,'categoryRelevant':True,'recommendedChanges':change,'sourceReview':'Everyday computing fact checked against the identified official vendor or NCSC reference; specific pages were used for percentages, extensions, transitions, email addressing, bookmarks, ZIP archives and SSIDs. Broad user guides are background references, not claimed per-sentence citations.'})
(p/'independent-review.json').write_text(json.dumps({'independent':False,'reviewer':'root (author second editorial pass)','status':'complete','reviewed':100,'remaining':0,'sourceAccessNote':'Official Microsoft, Mozilla, Apple and NCSC indexed documentation inspected. This is an author final check, not an independent reviewer. Stable ordinary interface definitions also checked directly for answer uniqueness.','rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Computers: 100 individual author-final-check decisions recorded')
