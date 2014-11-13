import datetime

class Target(object):
    def __init__(self, global_config, target_config):
        self.combine_config_options(global_config, target_config)

    def check_config_options(self):
        """
        Checking for the required target options.
        """
        required_options = ['slug', 'url']

        for option in required_options:
            try:
                option in self
            except KeyError:
                raise RuntimeError('Required option %s missing' % option)

    def combine_config_options(self, global_config, target_config):
        """
        Creates options for the target, prioritizing target-specific
        options over global options.
        """
        options_whitelist = ['page_load_delay', 'wait_for_js_signal', 'local_image_directory', 'aws_subpath', 'override_css_file', 'wait_for_js_signal', 'failure_timeout']

        for option in options_whitelist:
            self[option] = global_config[option]

        for option in target_config:
            self[option] = target_config[option]

    def filepath(self):
        """
        Generates a filepath for the image in the following form:

        slug/YYYY-MM-DD-HHMMSS-slug.png

        Used to generate local and aws filepaths.
        """
        current_datetime_string = get_current_datetime_string()
        slug = self.slug
        return '%s/%s-%s.png' % (slug, current_datetime_string, slug)

    def generate_image_local_filepath(self):
        """
        Generates a local filepath for the image, using
        `generate_image_filepath()`
        """
        local_image_directory = self.local_image_directory
        image_filepath = self.filepath()
        return '%s/%s' % (local_image_directory, image_filepath)

    def generate_image_aws_filepath(self):
        """
        Generates an aws filepath for the image, using
        `generate_image_filepath()`
        """
        aws_subpath = self.aws_subpath
        image_filepath = self.filepath()
        return '%s/%s' % (aws_subpath, image_filepath)

    def generate_image_aws_latest_filepath(self):
        """
        Generates an aws "latest" filepath for the image.
        """
        aws_subpath = self.aws_subpath
        slug = self.slug
        return '%s/%s/latest-%s.png' % (aws_subpath, slug, slug)

    def generate_public_url(self):
        """
        Generates a public URL for the file.
        """
        aws_bucket = self.aws_bucket
        aws_subpath = self.aws_subpath
        return 'http://s3.amazonaws.com/%s/%s' % (aws_bucket, aws_filepath)

def get_current_datetime_string():
    """
    Returns the current time in a string suitable for filenames.
    """
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d-%H%M%S')