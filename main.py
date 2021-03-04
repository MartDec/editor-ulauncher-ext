from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

from helpers import *
import os

class AtomExtension(Extension):

    def __init__(self):
        super(AtomExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = getDirectoryItems(extension.preferences['workspace_path'], is_index=True)
        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()

        if 'open_atom' in data:
            subprocess.run([extension.preferences['application_bin'], data['path']])
        else:
            actions = getResultItems(data, extension.preferences['workspace_path'])
            return RenderResultListAction(actions)


if __name__ == '__main__':
    AtomExtension().run()
