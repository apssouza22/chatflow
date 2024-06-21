import re

from core.agency.agents import AgentBase, Task
from core.docs_search.doc_service import Doc


class DocPickerAgent(AgentBase):
    def __init__(self, name, llm_service):
        super().__init__(name, llm_service)
        self.system_prompt = f"You are a DocPicker. You are a bot that helps users to pick the right document from a list of documents."
        f"Your job is to help users pick the right document from a list of documents. You will be given a list of documents and you will be asked to pick the right document based on the given prompt."

    def process(self, task: Task) -> Task:
        msg = self._build_message(task.input, task.context)

        infer = self.llm_service.infer([
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": msg}
        ])
        doc = self._filter_doc(task.context, infer.message)
        task.set_output(doc)
        return task

    @staticmethod
    def _build_message(txt_input, context: list[Doc]):
        contents = ""
        for i, doc in enumerate(context):
            contents += f"**Option {i}** - {doc.text}\n\n"

        msg = f"Given the following documents, please pick the right one to answer the following user input:  {txt_input}"
        msg = msg + """
        DOCUMENTS 
        ____
        """ + contents
        msg = msg + ("\n\nIMPORTANT: You must respond only with the option number (int type) of the document you think is the right one. nothing else."
                     "\nFor example, if you think the right document is the first one, you MUST respond with '0'."
                     "\n\n RESPONSE FORMAT: '0' or '1' or '2'. \n\n")

        return msg

    @staticmethod
    def _filter_doc(docs: list[Doc], text):
        match = re.findall(r'\d+', text)
        if len(match) == 0:
            return docs[0]

        for index, doc in enumerate(docs):
            if index == int(match[0]):
                return doc

        return docs[0]
