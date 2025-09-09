import os
from openai import OpenAI
from xoxxox.shared import Custom, LibLog

#---------------------------------------------------------------------------

class TttPrc:
  def __init__(self, config="xoxxox/config_tttgpt_cmm001", **dicprm):
    diccnf = Custom.update(config, dicprm)
    self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"] )
    self.mdlold = ""
    self.conlog = {}

  def status(self, config="xoxxox/config_tttgpt_cmm001", **dicprm):
    diccnf = Custom.update(config, dicprm)
    self.nmodel = diccnf["nmodel"]
    self.maxtkn = diccnf["maxtkn"]
    self.numtmp = diccnf["numtmp"]
    self.expert = diccnf["expert"]
    if not (self.expert in self.conlog):
      self.conlog[self.expert] = LibLog.getlog(diccnf["conlog"]) # LOG
      self.conlog[self.expert].catsys(diccnf) # LOG

  def infere(self, txtreq):
    prompt = self.conlog[self.expert].catreq(txtreq) # LOG
    print("prompt[", prompt, "]", sep="", flush=True) # DBG
    rawifr = self.client.chat.completions.create(
      model=self.nmodel,
      messages=prompt,
      max_tokens=self.maxtkn,
      temperature=self.numtmp
    )
    print("rawifr[", rawifr, "]", sep="", flush=True) # DBG
    txtifr = rawifr.choices[0].message.content
    print("txtifr[" + txtifr + "]", flush=True) # DBG
    txtres, txtopt = self.conlog[self.expert].arrres(txtifr) # LOG
    print("txtres[" + txtres + "]", flush=True) # DBG
    print("txtopt[" + txtopt + "]", flush=True) # DBG
    self.conlog[self.expert].catres(txtres) # LOG
    return (txtres, txtopt)
