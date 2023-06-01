// api/api.js

const API_BASE_URL = 'http://10.4.41.51:8000'; // Replace with your API base URL



export const getPosts = async (page = 1, pageSize = 10) => {
    try {
      const url = new URL(`${API_BASE_URL}/posts`);
      url.searchParams.append('page', page);
      url.searchParams.append('pageSize', pageSize);
        
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        throw new Error('Failed to fetch posts');
      }
    } catch (error) {
      console.error(error);
      throw new Error('Failed to fetch posts');
    }
  };

  

export const getTransactions = async (params) => {
  try {
    const url = new URL(`${API_BASE_URL}/posts`);
    if (params) {
      Object.keys(params).forEach((key) => url.searchParams.append(key, params[key]));
    }

    const response = await fetch(url);
    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      throw new Error('Failed to fetch posts');
    }
  } catch (error) {
    console.error(error);
    throw new Error('Failed to fetch posts');
  }
};

export const createPost = async (postData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/posts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData),
    });
    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      throw new Error('Failed to create post');
    }
  } catch (error) {
    console.error(error);
    throw new Error('Failed to create post');
  }
};
