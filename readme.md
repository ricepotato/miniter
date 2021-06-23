# miniter

## ping
`http -v GET localhost:5000/ping`

## sign-up

`http -v POST localhost:5000/sign-up name=sukjun.sagong eamil=sukjun40@naver.com`
`http -v POST localhost:5000/sign-up name=sukjun.sagong2 eamil=sukjun402@naver.com`

## tweet post

`http -v POST localhost:5000/tweet id:=1 tweet="my tweet2"`


## follow

`http -v POST localhost:5000/follow id:=1 follow:=2`


## unfollow

`http -v POST localhost:5000/unfollow id:=1 follow:=2`