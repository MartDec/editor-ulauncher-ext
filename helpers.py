from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction

import subprocess
import os

def getSubdirectories(root):
    results = []
    items = os.listdir(root)

    for item in items:
        fullPath = root + item
        if os.path.isdir(fullPath):
            results.append({
                'name': item,
                'path': fullPath
            })

    return results

def getResultItem(itemData):
    return ExtensionResultItem(
        icon='images/icon.svg',
        name=itemData['name'],
        description='%s directory' % itemData['name'],
        on_enter=ExtensionCustomAction(itemData, keep_app_open=True)
    )

def getDirectoryItems(root, is_index=False):
    directories = getSubdirectories(root)
    results = []
    for directory in directories:
        item = getResultItem(directory)
        results.append(item)

    return results

def getResultItems(data, workspacePath):
    items = getDirectoryItems('%s/' % data['path'])
    if data['path'] != workspacePath:
        items.insert(0, ExtensionResultItem(
            icon='images/back.svg',
            name='Go back',
            description='Go back to parent directory',
            on_enter=RenderResultListAction(getDirectoryItems('%s/../' % data['path']))
        ))

    actions = [
        ExtensionResultItem(
            icon='images/technology.svg',
            name=data['name'],
            description='Directory %s' % data['name'],
            on_enter=DoNothingAction()
        ),
        ExtensionResultItem(
            icon='images/back.svg',
            name='Go back',
            description='Go back to parent directory',
            on_enter=RenderResultListAction(getDirectoryItems('%s/../' % data['path']))
        ),
        ExtensionResultItem(
            icon='images/icon.svg',
            name='Open in your editor',
            description='Open directory %s in your editor' % data['name'],
            on_enter=ExtensionCustomAction(
                {
                    'open_editor': True,
                    'path': data['path']
                },
                keep_app_open=True
            )
        ),
        ExtensionResultItem(
            icon='images/project.svg',
            name='Display directory content',
            description='Display content of directory %s' % data['name'],
            on_enter=RenderResultListAction(items)
        )
    ]

    return actions
