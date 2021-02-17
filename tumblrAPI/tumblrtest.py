import pytumblr
client = pytumblr.TumblrRestClient(
  'KD3YxdO7uigsFn9v8iWD8KHEJIhlJpj4WUfDYXLX0KulX540Bg',
  'oACAMUWjAilXiIglpGh2ibZLJwwGrqRu4y9dpNJE28VjR4FLgu',
  'prHg38NXZQigKYFgxxKxLGO0ePkwksqLkjF9NI653ZbIKB27tx',
  'pdwCtHPdCZO1J5MxSkoWr4lunFjGx4gxbcUn4Y5Axi2b1BJScN'
)


print(client.posts('a-lil-perspective.tumblr.com', type='text', tag='I love these two', limit=2, filter='text'))