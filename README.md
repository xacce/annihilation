# Sources:

### annihilation.sources.native_xml.Xml
Native xml, using xmltodict library

```
sources:
  habr:
    class: annihilation.sources.native_xml.Xml
    url: https://habr.com/rss/hubs/all/
```


### class: annihilation.sources.rss.Rss
Feedparser library

```
sources:
  habr:
    class: annihilation.sources.rss.Rss
    url: https://habr.com/rss/hubs/all/
```

# Destinations

## annihilation.destinations.to_django.CurrentEnvironment
Write all to data to current django app models

1. Put `annihilation.django_annihilation` to INSTALLED_APPS

2. Call ./manage.py annihilate YAML_CONFIG_PATH

Perfomance tip:
    Default django not provide object pk after bulk create. Only worked for django >=1.10 and postgresql

Example:
```
destinations:
  django:
    class: annihilation.destinations.to_django.CurrentEnvironment
```

# Decomposers

```
decomposers:
  tags:
    mapper: annihilation.mappers.simple.Assoc
    source: habr.entries.*.tags.*
    destination:
      django:
        model: test_app.Tag
        unique_field: name

    mapping:
      name: term
      slug:
        from: term
        tuners:
          - slugify

  authors:
    mapper: annihilation.mappers.simple.Assoc
    source: habr.entries.*.authors.*
    destination:
      django:
        model: test_app.Author
        unique_field: username

    mapping:
      username: name

  entries:
    using:
      - tags
      - authors
    mapper: annihilation.mappers.simple.Assoc
    source: habr.entries.*
    destination:
      django:
        model: test_app.Entry
        unique_field: extra_id
    filters:
      - required: title
      - timedelta:
          field: published
          seconds: 86400
      - pre_contains:
          field: tags.*.term
          contains: Unity3D
    mapping:
      published:
        from: published
        tuners:
          - datetime: "%a, %d %b %Y %H:%M:%S %Z"
      content: summary_detail.value # or summary
      extra_id: id
      title: title
      tags:
        using: tags
        query: tags.*.term
        setter: m2m
      authors:
        using: authors
        query: authors.*.name
        setter: m2m
```

Keys: tags, authors, entries - you custom names, using form2m relations

* mapper: path to mapper class
* source: name of source (see Sources)
* destination:
```
    destination:
      django:
        model: test_app.Entry
        unique_field: extra_id
``
* using: if u decomposer used other decomposers then you must provide names here
* filters: Filter sources and save suitable data


## Mapping:

### Syntax:

```
# Data will be getting from "publushed_from" value and put to "published_to" field
published_to:
    from: published_from
# Same:
published_to: published_from
```
### Walking:

```
author: author.information.public.name. # Value will be getting from {'author':{'information':{'public':{'name':'Jimmy'}}}}
```

### Tuners:

```
  published:
    from: published
    tuners:
      - datetime: "%a, %d %b %Y %H:%M:%S %Z"

    #Value will be converted to python datetime object before saving
```


### m2m

```
  authors (ManyToMany field name (for django)):
    using: authors (see using directive)
    query: authors.*.name ( sub query from sources)
    setter: m2m (setter method, now supported only m2m
```
