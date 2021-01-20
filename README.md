# MyFirstPythonProject
---
### Intro
A service recording tasks & their status


### Hosting Server
Requirements:
* Docker version 19.03.5
* docker-compose version 1.25.4

Build images

```sh
$ cd MyFirstPythonProject
$ docker-compose build
```

Spin up servers

```sh
$ docker-compose up
```

### Test

Run unit test with coverage report on console

```sh
$ cd MyFirstPythonProject
$ export EXE_ENV=testing
$ pytest -p no:warnings --cov-report term-missing --cov=app ./tests/
```

### How to use
#### <span style="color:blue">POST</span> /task
Request Body
```yaml
{
  'name': 'task_name'
}
```
Response Code 201

Response Body
```yaml
{
  'id': 1,
  'name': 'task_name',
  'status': 0
}
```

#### <span style="color:blue">GET</span> /tasks
Request Body
None

Response Code 200

Response Body
```yaml
{
  'result': [
    {'id': 1, 'name': 'task1', 'status': 0}, 
    {'id': 2, 'name': 'task2', 'status': 0}
  ]
}
```

#### <span style="color:blue">PUT</span> /task/<id>
Request Body
```yaml
{
  'id': 1,
  'name': 'new_name',
  'status': 1
}
```

Response Code 200

Response Body
```yaml
{
  'id': 1,
  'name': 'new_name',
  'status': 1
}
```

#### <span style="color:blue">DELETE</span> /task/<id>
Request Body
None

Response Code 200

Response Body
None

License
----

MIT

**Free Software, Hell Yeah!**
