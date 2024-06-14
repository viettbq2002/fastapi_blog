from tests.utils.blog import create_random_blog


def test_should_fetch_blog_created(client, db_session):
    blog = create_random_blog(db=db_session)
    response = client.get(f"/blogs/{blog.id}")
    assert response.status_code == 200
    assert response.json()["title"] == blog.title
