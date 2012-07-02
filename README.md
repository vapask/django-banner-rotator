README
======

Banner Rotation App for Django.

* Tracks clicks and views.
* Supports the weight of the banner, banners with large weight are shown more often.
* You can create ad campaigns.


Setup
======

Get the code via git:

    git clone git://github.com/vapask/django-banner-rotator.git django-banner-rotator

Add the django-banner-rotator/banner_rotator folder to your PYTHONPATH.

Or get app via pip:

    pip install -e git+git://github.com/vapask/django-banner-rotator.git#egg=django-banner-rotator

Add "banner_rotator" to INSTALLED_APPS:

    INSTALLED_APPS = (

        "banner_rotator",

    )

Edit urls.py:

    urlpatterns = patterns('',

        url(r'^banner_rotator/', include('banner_rotator.urls')),

    )

Add to the template:

    {% load banners %}
    {% banner place-slug %}

or manually:

    {% load banners %}
    {% banner place-slug as banner %}
    <a href="{% url banner_click banner.id %}?place_slug=place-slug"><img src="{{ banner.file.url }}" alt=""/></a>

