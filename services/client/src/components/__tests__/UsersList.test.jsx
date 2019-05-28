import React from 'react';
import { shallow } from 'enzyme';


import UsersList from '../UsersList';

const users = [
  {
    'active': true,
    'email': 'claribel@gmail.com',
    'id': 1,
    'username': 'claribel'
  },
  {
    'active': true,
    'email': 'lilianainfante@upeu.edu.pe',
    'id': 2,
    'username': 'liliana'
  }
];

test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe('claribel');
});
