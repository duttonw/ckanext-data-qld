import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import datetime

from ckan.common import c, config
from pylons import request

def get_gtm_code():
    # To get Google Tag Manager Code
    gtm_code = config.get('ckan.google_tag_manager.gtm_container_id', False)
    return str(gtm_code)


def get_year():
    now = datetime.datetime.now()
    return now.year


def ytp_comments_enabled():
    return "ytp_comments" in config.get('ckan.plugins', False)


def get_all_groups():
    groups = toolkit.get_action('group_list')(
        data_dict={'include_dataset_count': False, 'all_fields': True})
    pkg_group_ids = set(group['id'] for group
                        in c.pkg_dict.get('groups', []))
    return [[group['id'], group['display_name']]
            for group in groups if
            group['id'] not in pkg_group_ids]

def is_request_for_resource():
    original_request = request.environ.get('pylons.original_request') 
    dataset_found = False
    resource_found = False   
    # Searching for a url path for /dataset/ and /resource/
    # eg. /dataset/test-dataset-name/resource/b33a702a-f162-44a8-aad9-b9e630a8f56e
    for path in original_request.path.split('/'):
        if 'dataset' == path.lower():
            dataset_found = True
        elif dataset_found and 'resource' == path.lower(): #dataset path must be found before resource path to be valid
            resource_found = True
            break    

    return dataset_found and resource_found


class DataQldThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'data_qld_theme')

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_gtm_container_id': get_gtm_code,
            'get_year': get_year,
            'ytp_comments_enabled': ytp_comments_enabled,
            'get_all_groups': get_all_groups,
            'is_request_for_resource': is_request_for_resource
        }
