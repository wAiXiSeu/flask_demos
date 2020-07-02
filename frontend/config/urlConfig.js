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
  },
  emr: {
    list_emr: BACK_END_BASE_URL + "syf/list ",
    get_emr: BACK_END_BASE_URL + "syf/case",
    get_basic_info: BACK_END_BASE_URL + "syf/basic",
    get_fields: BACK_END_BASE_URL + "syf/fields",
    get_emrx: BACK_END_BASE_URL + "syf/casex",
  }
};

export default SERVICE_URL;

