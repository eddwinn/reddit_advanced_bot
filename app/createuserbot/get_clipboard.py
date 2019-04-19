import subprocess


def getClipboardData():
    p = subprocess.Popen(['xclip','-o'], stdout=subprocess.PIPE)

    retcode = p.wait()
    data = p.stdout.read()

    return data.decode("utf-8")

