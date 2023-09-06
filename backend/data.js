import bcrypt from 'bcryptjs';

const data = {
  users: [
    {
      name: 'Thanu',
      email: 'admin@admin.com',
      password: bcrypt.hashSync('123456'),
      isAdmin: true,
    },
    {
      name: 'Joe',
      email: 'joe@joe.com',
      password: bcrypt.hashSync('123456'),
      isAdmin: false,
    },
  ],
  products: [
    {
      name: 'A-Level Book',
      slug: 'a-level-book',
      category: 'books',
      image: '/images/b1.jpg',
      price: 120,
      countInStock: 10,
      rating: 4.5,
      numReviews: 10,
      description: 'A-level computer science textbook',
    },
    {
      name: 'GCSE Book',
      slug: 'gcse-book',
      category: 'books',
      image: '/images/b2.jpg',
      price: 120,
      countInStock: 0,
      rating: 4.5,
      numReviews: 10,
      description: 'GCSE computer science textbook',
    },
    {
      name: 'University Book',
      slug: 'uni-book',
      category: 'books',
      image: '/images/b3.jpg',
      price: 120,
      countInStock: 20,
      rating: 4.5,
      numReviews: 10,
      description: 'University computer science textbook',
    },
  ],
};
export default data;
