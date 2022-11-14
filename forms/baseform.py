from wtforms import Form


# 用于从form.errors中提取所有字符串类型的错误信息
# 以后可以通过form.messages得到所有字符串类型的错误信息，用于传递给渲染模板
class BaseForm(Form):
    @property
    def messages(self):
        message_list = []
        if self.errors:
            for error in self.errors.values():
                message_list.extend(error)
        return message_list
