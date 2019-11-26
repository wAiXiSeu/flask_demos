let BACK_END_BASE_URL = '';

if (process.env.NODE_ENV === 'development') {
  BACK_END_BASE_URL = 'http://localhost:12345/';
} else if (process.env.NODE_ENV === 'production') {
  BACK_END_BASE_URL = '/api/';
}

let SERVICE_URL = {
  dockers: {
    list_images: BACK_END_BASE_URL + "docker/images/list",
    delete_images: BACK_END_BASE_URL + "docker/images/delete"
  }
};

export default SERVICE_URL;

