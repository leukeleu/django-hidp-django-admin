from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


def _is_excluded(name):
    # Exclude files that are part of the Vue.js frontend build.
    # These files are already hashed by Vite. Hashing them again is
    # unnecessary and can cause issues with dynamic imports.
    # See also: https://github.com/MrBin99/django-vite/issues/86#issuecomment-1750063192
    return name.startswith("vue/")


class SelectiveManifestStaticFilesStorage(ManifestStaticFilesStorage):
    """
    A static files storage backend that excludes certain files from hashing.
    """

    def hashed_name(self, name, content=None, filename=None):
        if _is_excluded(name):
            return name
        else:
            return super().hashed_name(name, content, filename)
