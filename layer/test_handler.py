import os
def test_handler():
    import settings
    keys = [k for k in os.environ if 'CHANNEL' in k]
    return f'imported settings: {keys}'