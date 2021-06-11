let BACK_END_BASE_URL = '';

if (process.env.NODE_ENV === 'development') {
  BACK_END_BASE_URL = 'http://localhost:12345/';
} else if (process.env.NODE_ENV === 'production') {
  BACK_END_BASE_URL = '/api/';
}

let SERVICE_URL = {
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

