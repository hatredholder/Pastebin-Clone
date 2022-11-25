import datetime

from wtforms.fields import StringField


def check_paste_title(title):
    """Returns 'Untitled' if title wasn't provided"""
    return title if title else "Untitled"


def check_if_paste_exists(paste):
    """Returns True if paste exists and vice versa"""
    return bool(paste)


def check_paste_expiration(paste):
    """Deletes the paste if its expired and returns to not_found"""
    if (
        paste.paste_expiration > 0
        and datetime.datetime.now()
        > paste.created
        + datetime.timedelta(
            seconds=paste.paste_expiration,
        )
    ):
        paste.delete()
        return True
    else:
        return False


class TagListField(StringField):
    """Stringfield for a list of separated tags"""

    def __init__(
        self,
        label="",
        validators=None,
        remove_duplicates=True,
        to_lowercase=True,
        separator=" ",
        **kwargs,
    ):
        """
        Construct a new field.
        :param label: The label of the field.
        :param validators: A sequence of validators to call when validate is called.
        :param remove_duplicates: Remove duplicates in a case insensitive manner.
        :param to_lowercase: Cast all values to lowercase.
        :param separator: The separator that splits the individual tags.
        """
        super(TagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates
        self.to_lowercase = to_lowercase
        self.separator = separator
        self.data = []

    def _value(self):
        if self.data:
            return ", ".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(self.separator)]
            if self.remove_duplicates:
                self.data = list(self._remove_duplicates(self.data))
            if self.to_lowercase:
                self.data = [x.lower() for x in self.data if x != ""]

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item
