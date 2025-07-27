import os
from openai import OpenAI
from xoxxox.shared import Custom

#---------------------------------------------------------------------------

class TttPrc:

  def __init__(self, config="xoxxox/config_tttgpt_000", **dicprm):
    diccnf = Custom.update(config, dicprm)
    self.nmodel = diccnf["nmodel"]
    self.maxlen = 40
    self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"] )

  def status(self, config="xoxxox/config_tttgpt_000", **dicprm):
    diccnf = Custom.update(config, dicprm)
    self.nummax = diccnf["prmmax"]
    self.txtsys = diccnf["status"]
    self.txtadd = diccnf["rolslf"]
    self.txtdel = diccnf["roloth"]

    self.txtdef = "："
    self.lstlog = []

  def infere(self, txtreq):
    lstmsg = []
    prompt = self.txtadd + self.txtdef + txtreq
    lstmsg.append({"role": "system", "content": self.txtsys})
    lstmsg.extend(self.lstlog)
    lstmsg.append({"role": "user", "content": prompt})
    jsnans = self.client.chat.completions.create(
      model=self.nmodel,
      messages=lstmsg,
      max_completion_tokens=self.maxlen
    )
    #print("lstmsg[" + str(lstmsg) + "]") # DBG
    txtans = jsnans.choices[0].message.content
    self.lstlog.append({"role": "user", "content": prompt})
    self.lstlog.append({"role": "assistant", "content": txtans})
    if len(self.lstlog) >= self.nummax + 2:
      self.lstlog.pop(0)
      self.lstlog.pop(0)
    txtres = txtans.replace(self.txtdel + self.txtdef, "")
    #print("txtreq[" + txtreq + "]") # DBG
    #print("txtres[" + txtres + "]") # DBG
    return txtres
