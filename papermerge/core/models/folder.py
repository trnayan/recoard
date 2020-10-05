from django.utils.translation import ugettext_lazy as _
from papermerge.core.models.diff import Diff
from papermerge.core.models.kvstore import KVCompNode, KVNode, KVStoreNode
from papermerge.core.models.node import BaseTreeNode
from papermerge.search import index


class Folder(BaseTreeNode, index.Indexed):

    INBOX_NAME = "inbox"

    search_fields = [
        index.SearchField('title'),
        index.SearchField('text', partial_match=True, boost=2),
        index.SearchField('notes')
    ]

    def to_dict(self):
        item = {}

        item['id'] = self.id
        item['title'] = self.title
        item['created_at'] = self.created_at.strftime("%d.%m.%Y %H:%M:%S")
        item['timestamp'] = self.created_at.timestamp()

        if self.parent:
            item['parent_id'] = self.parent.id
        else:
            item['parent_id'] = ''
        item['ctype'] = 'folder'

        tags = []
        for tag in self.tags.all():
            tags.append(tag.to_dict())
        item['tags'] = tags

        return item

    @property
    def kv(self):
        return KVNode(instance=self)

    @property
    def kvcomp(self):
        return KVCompNode(instance=self)

    def inherit_kv_from(self, folder):
        instances_set = []

        for key in folder.kv.keys():
            instances_set.append(
                KVStoreNode(key=key, kv_inherited=True, node=self)
            )

        # if there is metadata
        if len(instances_set) > 0:
            diff = Diff(
                operation=Diff.ADD,
                instances_set=instances_set
            )

            self.propagate_changes(
                diffs_set=[diff],
                apply_to_self=True
            )

    class Meta:
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        return self.title
