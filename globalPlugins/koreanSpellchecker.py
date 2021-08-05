import inputCore
import ui
import json
import urllib
import textInfos
import api
import globalPluginHandler
from scriptHandler import script

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@script(gesture='kb:nvda+f8', description='맞춤법을 검사합니다.', category=inputCore.SCRCAT_MISC)
	def script_checkSpellOut(self, gesture):
		info = api.getReviewPosition()
		info.expand(unit=textInfos.UNIT_PARAGRAPH)
		paraText = info.text
		if not paraText.strip():
			ui.message('검사할 문자열이 없습니다.')
			return
		data = 'text1=' + paraText
		data = data.encode('utf8')
		res = urllib.request.urlopen('https://speller.cs.pusan.ac.kr/results', data)
		htm = res.read().decode('utf8')
		start = htm.find('data = [{')
		if start == -1:
			ui.message('맞춤법이 정확합니다.')
			return
		end = htm.find('}];', start)
		errData = htm[start+7:end+2]
		errObj = json.loads(errData)
		errList = errObj[0]['errInfo']
		resultList = ['<p>틀린 문구: %s</p><p>추천 문구: %s</p><p>도움말: %s</p><p>--- 항목 끝 ---</p>' % (d['orgStr'], d['candWord'], d['help']) for d in errList]
		ui.browseableMessage('\n'.join(resultList), '맞춤법 검사 결과', isHtml=True)
