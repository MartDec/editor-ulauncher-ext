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
        icon='images/directory.svg',
        name=itemData['name'],
        description='%s directory' % itemData['name'],
        on_enter=ExtensionCustomAction(itemData, keep_app_open=True)
    )

def getDirectoryItems(root, workspaceRoot, avoid_loop=False):
    root = '%s/' % os.path.realpath(root)
    print('root %s' % root)
    print('workspaceRoot %s' % workspaceRoot)
    directories = getSubdirectories(root)
    results = []
    if root != workspaceRoot:
        results.append(ExtensionResultItem(
            icon='images/back.svg',
            name='Go back',
            description='Go back to parent directory',
            on_enter=RenderResultListAction(getDirectoryItems('%s/../' % root, workspaceRoot, not avoid_loop))
        ))

    for directory in directories:
        item = getResultItem(directory)
        results.append(item)

    return results

def getResultItems(data, workspaceRoot):
    actions = [
        ExtensionResultItem(
            icon='images/technology.svg',
            name=data['name'],
            description='Directory %s' % data['name'],
            on_enter=DoNothingAction()
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
        )
    ]
    items = getDirectoryItems('%s/' % data['path'], workspaceRoot)
    actions.extend(items)

    return actions
