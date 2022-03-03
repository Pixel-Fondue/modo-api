#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.
#

"""

.. module:: modo.dialogs
   :synopsis: Functions to display the various modo dialog types.

.. moduleauthor:: Gwynne Reddick <gwynne.reddick@thefoundry.co.uk>

"""

import lx

cmdSvc = lx.service.Command()
dialogSvc = lx.service.StdDialog()

globalInterpreter = True
try:
    import lxifc
except:
    globalInterpreter = False


def cmd(evalString):
    if globalInterpreter:
        cmdSvc.ExecuteArgString(-1, lx.symbol.iCTAG_NULL, evalString)
    else:
        lx.eval(evalString)


def customFile(dtype, title, names, unames, patterns=None, ext=None, path=None):
    """Displays a file open or file save dialog for one or more custom file types.

    :returns: A single file path for "fileSave' and 'fileOpen' dialogs, a list of file paths for 'fileOpenMulti'
        dialogs or 'None' if dialog is cancelled by the user.
    :rtype: string or None
    :param dtype: Dialog type, string, one of 'fileOpen', 'fileOpenMulti' or 'fileSave'.
    :type dtype: string.
    :param title: Dialog title.
    :type title: string.
    :param names: List or tuple of file format type names. This is an internal name for use by  the script, and can be
        read out after the dialog is dismissed by  querying  dialog.fileSaveFormat.
    :type names: list or tuple of strings.
    :param unames: List of user names that will be displayed in the dialog for each of the types specified in ftype.
    :type unames: list or tuple of strings.
    :param patterns: Optional collection of semicolon-delimited string lists of file extensions that the particular
        file format supports. Only used for fileOpen dialogs. Each extension must include a leading asterisk and period
        for the filtering to work properly, such as '*.jpg;*.jpeg'.
    :type patterns: list or tuple of strings.
    :param ext: Optional collection of save extensions, one for each of the types specified in ftype. each ext is a
        single file extension that will automatically be appended to the end of the filename selected in a save dialog.
        The period should not be entered, just the extension such as lwo, tga  or txt.
    :type ext: list or tuple of strings.
    :param path: Optional default path to open the dialog at.
    :type path: string.

    File open examples::

        # Single file format
        inpath = modo.dialogs.customFile('fileOpen', 'Open File', ('text',), ('Text File',), ('*.txt',))

        # Multiple file formats
        inpath = modo.dialogs.customFile('fileOpen', 'Open File', ('text', 'html',),
                                   ('Text File', 'HTML FIle'), ('*.txt', '*.html',))

        # open multiple files
        inpaths = modo.dialogs.customFile('fileOpenMulti', 'Open File', ('text',), ('Text File',), ('*.txt',))

    File save examples::

        # Single file format
        outpath = modo.dialogs.customFile('fileSave', 'Save File', ('text',), ('Text File',), ext=('txt',))

        #Multiple file formats
        outpath = modo.dialogs.customFile('fileSave', 'Save File', ('text', 'html',),
                                    ('Text File', 'HTML FIle'), ext=('txt', 'html',))

    """

    cmd('dialog.setup {0:s}'.format(dtype))
    cmd('dialog.title {{{0:s}}}'.format(title))
    for index, name in enumerate(names):
        if dtype == 'fileSave':
            cmd('dialog.fileTypeCustom {{{0:s}}} {{{1:s}}} "" {{{2:s}}}'.format(name,unames[index],ext[index]))
        else:
            cmd('dialog.fileTypeCustom {{{0:s}}} {{{1:s}}} {{{2:s}}} ""'.format(name, unames[index], patterns[index]))

    if path:
        cmd('dialog.result {{{0:s}}}'.format(path))
    try:
        cmd('dialog.open')
    except RuntimeError as e:
        if str(e) == 'bad result: RENDER_ABORTING':
            return None
        else:
            raise
    command = cmdSvc.Spawn(lx.symbol.iCTAG_NULL, 'dialog.result')
    valArray = cmdSvc.Query(command, 0)
    if valArray.Count() > 0:
        if dtype == 'fileOpenMulti':
            return [valArray.GetString(x) for x in range(valArray.Count())]
        return valArray.GetString(0)


def fileOpen(ftype, title='Open File(s)', multi=False, path=None):
    """ Display a dialog to choose a file or files for opening.

    :returns: Single file path if 'multi' is False, list of files paths if 'multi' is true or 'None' if the dialog is
        cancelled by the user.
    :rtype: string or None
    :param ftype: File format type to filter on or None to show all files.
    :type ftype: string
    :param title: Dialog title.
    :type title: str
    :param multi: Enable multi-select of files in the dialog.
    :type multi: Boolean
    :param path: Optional path to open the dialog at.
    :type path: str

    Open dialogs use a file type to filter the load dialog. A file type is the class of data to be loaded or saved,
    such as an image or an object and should be one of the known file types, such as text, script, config,
    macro, image, and so on. Also, the name of any specific loader plug-in can also be used, such as $LWO. If no
    file type is set, all files will be shown.

    """
    if multi:
        cmd('dialog.setup fileOpenMulti')
    else:
        cmd('dialog.setup fileOpen')
    cmd('dialog.title {{{0:s}}}'.format(title))
    cmd('dialog.fileType {{{0:s}}}'.format(ftype))

    if path:
        cmd('dialog.result {{{0:s}}}'.format(path))
    try:
        cmd('dialog.open')
    except RuntimeError as e:
        if str(e) == 'bad result: RENDER_ABORTING':
            return None
        else:
            raise
    command = cmdSvc.Spawn(lx.symbol.iCTAG_NULL, 'dialog.result')
    valArray = cmdSvc.Query(command, 0)
    if valArray.Count() > 0:
        if multi:
            return [valArray.GetString(x) for x in range(valArray.Count())]
        return valArray.GetString(0)


def fileSave(ftype, fformat, fspec='extension', title='Save File', path=None):
    """ Display a dialog to choose a filename to save to.

    :returns: file path or 'None' if dialog is cancelled by the user.
    :rtype: string or None
    :param ftype: File type to save as.
    :type ftype: string
    :param fformat: Default file format to save as
    :type fformat: string
    :param fspec: How the file format is specified, either by 'extension' for file extension or 'format' for file format
        name. Defaults to 'extension'.
    :type fspec: string
    :param title: Dialog title.
    :type title: string
    :param path: Optional default path to open the dialog at.
    :type path: string

    A save dialog is identical to an open dialog, but adds a save format to select a specific default file format
    within the file type to save as. This format will be selected by default when the dialog opens The file
    format can be set either by its default extension, which is the default behavior, or by the file format's
    internal name.

    """
    cmd('dialog.setup fileSave')
    cmd('dialog.title {{{0:s}}}'.format(title))
    cmd('dialog.fileType {{{0:s}}}'.format(ftype))
    cmd('dialog.fileSaveFormat {{{0:s}}} {{{1:s}}}'.format(fformat, fspec))
    if path:
        cmd('dialog.result {{{0:s}}}'.format(path))
    try:
        cmd('dialog.open')
    except RuntimeError as e:
        if str(e) == 'bad result: RENDER_ABORTING':
            return None
        else:
            raise
    command = cmdSvc.Spawn(lx.symbol.iCTAG_NULL, 'dialog.result')
    valArray = cmdSvc.Query(command, 0)
    if valArray.Count() > 0:
        return valArray.GetString(0)


def dirBrowse(title, path=None):
    """ Display a directory dialog.

    :returns: file path or 'None' if dialog is cancelled by the user.
    :rtype: string or None
    :param title: Dialog title string.
    :type title: string
    :param path: Optional default path to open the dialog at.
    :type path: string

    """
    cmd('dialog.setup dir')
    cmd('dialog.title {{{0:s}}}'.format(title))
    if path:
        cmd('dialog.result {{{0:s}}}'.format(path))
    try:
        cmd('dialog.open')
    except RuntimeError as e:
        if str(e) == 'bad result: RENDER_ABORTING':
            return None
        else:
            raise
    command = cmdSvc.Spawn(lx.symbol.iCTAG_NULL, 'dialog.result')
    valArray = cmdSvc.Query(command, 0)
    if valArray.Count() > 0:
        return valArray.GetString(0)


def alert(title, message, dtype='info'):
    """A simple alert dialog. Type can be any one of 'info', 'warning' or 'error' depending on the value passed for
    'dtype', defaults to 'info'

    :param title: Dialog title.
    :type title: string
    :param dtype: Dialog type. One of 'info', 'warning', 'error'. Defaults to 'info'
    :type dtype: string
    :param message: Dialog message.
    :type message: string

    """
    msg = dialogSvc.MessageAllocate()
    msg.SetMessage('common', '', 99)
    msg.SetArgumentString(1, message)
    if dtype == 'warning':
        msg.SetCode(lx.result.WARNING)
    elif dtype == 'error':
        msg.SetCode(lx.result.FAILED)
    else:
        msg.SetCode(lx.result.OK)
    dialogSvc.MessageOpen(msg, title, '', '')


def okCancel(title, message):
    """A two button OK/Cancel message dialog.

    :returns: 'ok' or 'cancel'
    :rtype: string
    :param title: Dialog title.
    :type title: string
    :param message: Dialog message.
    :type message: string

    """
    msg = dialogSvc.MessageAllocate()
    msg.SetMessage('common', '', 99)
    msg.SetArgumentString(1, message)
    msg.SetCode(lx.result.MSGDIALOG_AS_OKCANCEL)
    try:
        dialogSvc.MessageOpen(msg, title, '', '')
    except RuntimeError as e:
        if str(e) == 'bad result: MSGDIALOG_CANCEL':
            return 'cancel'
        else:
            raise
    return 'ok'


def yesNo(title, message):
    """A two button Yes/No message dialog.

    :returns: 'yes' or 'no'
    :rtype: string
    :param title: Dialog title.
    :type title: string
    :param message: Dialog message.
    :type message: string

    """
    msg = dialogSvc.MessageAllocate()
    msg.SetMessage('common', '', 99)
    msg.SetArgumentString(1, message)
    msg.SetCode(lx.result.MSGDIALOG_AS_YESNO)
    try:
        dialogSvc.MessageOpen(msg, title, '', '')
    except RuntimeError as e:
        if str(e) == 'bad result: MSGDIALOG_NO':
            return 'no'
        else:
            raise
    return 'yes'


def saveOK(title, message):
    """A Save OK dialog.

    :returns: 'save', 'no' or 'cancel'
    :rtype: string
    :param title: Dialog title.
    :type title: string
    :param message: Dialog message.
    :type message: string

    """
    msg = dialogSvc.MessageAllocate()
    msg.SetMessage('common', '', 99)
    msg.SetArgumentString(1, message)
    msg.SetCode(lx.result.MSGDIALOG_AS_SAVEOK)
    try:
        dialogSvc.MessageOpen(msg, title, '', '')
    except RuntimeError as e:
        if str(e) == 'bad result: MSGDIALOG_CANCEL':
            return 'cancel'
        elif str(e) == 'bad result: MSGDIALOG_NO':
            return 'no'
        else:
            raise
    return 'save'


def yesNoCancel(title, message):
    """A three button Yes/No/Cancel message dialog.

    :returns: 'yes', or 'cancel'
    :rtype: string
    :param title: Dialog title.
    :type title: string
    :param message: Dialog message.
    :type message: string

    """
    msg = dialogSvc.MessageAllocate()
    msg.SetMessage('common', '', 99)
    msg.SetArgumentString(1, message)
    msg.SetCode(lx.result.MSGDIALOG_AS_YESNOCANCEL)
    try:
        dialogSvc.MessageOpen(msg, title, '', '')
    except RuntimeError as e:
        if str(e) == 'bad result: MSGDIALOG_CANCEL':
            return 'cancel'
        elif str(e) == 'bad result: MSGDIALOG_NO':
            return 'no'
        else:
            raise
    return 'ok'


def yesAllCancel(title, message):
    """A three button Yes/Yes to all/Cancel dialog.

    :returns: 'yes', 'yesall' or 'cancel'
    :rtype: string
    :param title: Dialog title.
    :type title: string
    :param message: Dialog message.
    :type message: string

    """
    msg = dialogSvc.MessageAllocate()
    msg.SetMessage('common', '', 99)
    msg.SetArgumentString(1, message)
    msg.SetCode(lx.result.MSGDIALOG_AS_YESTOALLCANCEL)
    try:
        dialogSvc.MessageOpen(msg, title, '', '')
    except RuntimeError as e:
        if str(e) == 'bad result: MSGDIALOG_CANCEL':
            return 'cancel'
        else:
            raise
    return 'yes'


def yesNoAll(title, message):
    """A four option Yes/Yes to all/No/No to all dialog.

    :returns: 'yes', 'yestoall', 'no', 'notoall' or 'cancel'
    :rtype: string
    :param title: Dialog title.
    :type title: string
    :param message: Dialog message.
    :type message: string

    """
    msg = dialogSvc.MessageAllocate()
    msg.SetMessage('common', '', 99)
    msg.SetArgumentString(1, message)
    msg.SetCode(lx.result.MSGDIALOG_AS_YESNOALL)
    try:
        dialogSvc.MessageOpen(msg, title, '', '')
    except RuntimeError as e:
        if str(e) == 'bad result: MSGDIALOG_CANCEL':
            return 'cancel'
        elif str(e) == 'bad result: MSGDIALOG_NO':
            return 'no'
        elif str(e) == 'bad result: MSGDIALOG_NOTOALL':
            return 'notoall'
        else:
            raise
    return 'ok'


def yesnoToAll(title, message):
    """A three option Yes/No/No to all dialog.

    :returns: 'yes', 'noall' or 'cancel'
    :rtype: string
    :param title: Dialog title.
    :type title: string
    :param message: Dialog message.
    :type message: string

    """
    msg = dialogSvc.MessageAllocate()
    msg.SetMessage('common', '', 99)
    msg.SetArgumentString(1, message)
    msg.SetCode(lx.result.MSGDIALOG_AS_YESNOTOALL)
    try:
        dialogSvc.MessageOpen(msg, title, '', '')
    except RuntimeError as e:
        if str(e) == 'bad result: MSGDIALOG_CANCEL':
            return 'cancel'
        elif str(e) == 'bad result: MSGDIALOG_NO':
            return 'no'
        elif str(e) == 'bad result: MSGDIALOG_NOTOALL':
            return 'notoall'
        else:
            raise
    return 'ok'


