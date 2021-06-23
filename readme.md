# miniter

## ping
`http -v GET localhost:5000/ping`

## sign-up

`http -v POST localhost:5000/sign-up name=sukjun.sagong email=sukjun40@naver.com password=password1`
`http -v POST localhost:5000/sign-up name=sukjun.sagong2 email=sukjun402@naver.com password=password2`

## login

`http -v POST localhost:5000/login email=sukjun40@naver.com password=password1`

## tweet post

`http -v POST localhost:5000/tweet id:=1 tweet="my tweet2"`


## follow

`http -v POST localhost:5000/follow id:=1 follow:=2`


## unfollow

`http -v POST localhost:5000/unfollow id:=1 follow:=2`