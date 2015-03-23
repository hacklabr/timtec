from model_mommy import mommy


# def test_simple(timbrowser):
#     timbrowser.visit(timbrowser.url)
#     assert timbrowser.is_text_present('Timtec')


def test_login(timbrowser, user):
    b = timbrowser
    b.visit(b.url)
    b.find_by_xpath('//a[normalize-space(text())="Entrar"]').click()
    assert b.is_element_present_by_css('.open .dropdown-menu')
    b.fill('login', user.username)
    b.fill('password', 'password')
    b.find_by_css('.submit .btn-success').first.click()
    assert b.is_element_present_by_css('.username')


def test_courses_home(timbrowser):
    b = timbrowser
    mommy.make('Course', name='FindMe', home_published=True)

    b.visit(b.url)
    assert len(b.find_by_css('.course')) >= 1
    assert b.is_element_present_by_xpath('//h3[normalize-space(text())="FindMe"]')
