import logging
from helpers import validate_response

log = logging.getLogger(__name__)


def get_gists_count(gist):
    read_gist = gist.read_all()
    assert read_gist.status_code == 200
    read_gist_json = read_gist.json()
    return len(read_gist_json)


def test_crud_gist(gist):
    # Get current Gists for the user
    curr_gists = get_gists_count(gist)

    # Create new gist
    payload = {'description': 'Python TEST Gist',
               "public": False,
               'files': {
                   'hello_world.md': {
                       'content': 'Hello GIST World!'
                   },
                   'hello_second_world.md': {
                       'content': 'Hello GIST World!'
                   }
               }
               }

    create_gist = gist.create(body=payload)
    assert create_gist.status_code == 201
    create_gist_json = create_gist.json()
    gist_id = create_gist_json['id']

    new_gist_count = get_gists_count(gist)
    assert new_gist_count == curr_gists + 1
    validate_response(create_gist_json, payload)

    # Read created Gist
    read_gist = gist.read(gist_id)
    assert read_gist.status_code == 200
    read_gist_json = read_gist.json()
    validate_response(read_gist_json, payload)

    # Update Gist
    update_payload = {'description': 'Python TEST Gist UPDATE',
                      'files': {
                          'hello_world.md': {
                              'content': 'Hello GIST World UPDATE!',
                              'filename': 'hello_gist_world'
                          }
                      }
                      }
    update_gist = gist.update(gist_id, body=update_payload)
    assert update_gist.status_code == 200
    update_gist_json = update_gist.json()

    # Delete Gist
    delete_gist = gist.delete(gist_id)
    assert delete_gist.status_code == 204
    final_gist_count = get_gists_count(gist)
    assert final_gist_count == new_gist_count - 1
