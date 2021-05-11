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
    list_emr: BACK_END_BASE_URL + "syf/list",
    get_emr: BACK_END_BASE_URL + "syf/case",
    get_basic_info: BACK_END_BASE_URL + "syf/basic",
    get_fields: BACK_END_BASE_URL + "syf/fields",
    get_emrx: BACK_END_BASE_URL + "syf/casex",
  },
  tz: {
    list_vid: BACK_END_BASE_URL + "tz/vid",
    list_doc: BACK_END_BASE_URL + "tz/doc",
    list_details: BACK_END_BASE_URL + "tz/details",
  },
  testCases: {
    list_caseId: BACK_END_BASE_URL + "cases/list",
    get_emr: BACK_END_BASE_URL + "cases/emr",
    get_qc: BACK_END_BASE_URL + "cases/qc",
    delete_qcs: BACK_END_BASE_URL + "cases/delete",
    doctor_result: BACK_END_BASE_URL + "cases/doctor_result",
    download_qcs: BACK_END_BASE_URL + "cases/download",
  }
};

export default SERVICE_URL;

