<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8" style="display: flex; align-items: center; justify-content: space-between">
        <el-select v-model="selectedCaseId"
                   placeholder="请选择caseId"
                   @change="get_emr"
                   filterable>
          <el-option
            v-for="item in caseIds"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
        <el-select v-model="selectedDocId"
                   placeholder="请选择文档"
                   @change="get_doc"
                   filterable>
          <el-option
            v-for="item in docNames"
            :key="item.value"
            :label="item.key"
            :value="item.value">
          </el-option>
        </el-select>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12">
        <div v-html="htmlInfo"></div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  import axios from 'axios';
  import SERVICE_URL from "../../config/urlConfig";

  export default {
    name: "TZ",
    data() {
      return {
        emrRecords: {"inp_record": [], "first_page": []},
        currentInpRecord: "",
        currentFirstPage: "",
        caseIds: [],
        selectedCaseId: "",
        selectedDocId: "",
        docNames: [],
        htmlInfo: ''
      }
    },

    methods: {

      initCollection(){
        this.caseIds = [];
        this.selectedCaseId = "";
        this.docNames = [];
        axios.get(SERVICE_URL.tz.list_vid).then((response) => {
          if (response.status === 200) {
            for (let d of response.data.data) {
              this.caseIds.push(d);
            }
          }
          this.selectedCaseId = this.caseIds[0];
          axios.get(`${SERVICE_URL.tz.list_doc}?vid=${this.selectedCaseId}`).then((resp) => {
            if(resp.status===200){
              for (let t of resp.data.data) {
                this.docNames.push({
                  key: t,
                  value: t
                });
              }
            }
          }).catch(function (error) {
            console.log(error);
          });
        }).catch(function (error) {
          console.log(error);
        });
      },

      get_emr(){
        this.selectedDocId = '';
        this.docNames = [];
        this.htmlInfo = '';
        axios.get(`${SERVICE_URL.tz.list_doc}?vid=${this.selectedCaseId}`).then((resp) => {
          if(resp.status===200){
            for (let t of resp.data.data) {
              this.docNames.push({
                key: t,
                value: t
              });
            }
          }
        }).catch(function (error) {
          console.log(error);
        });
      },

      get_doc() {
        this.htmlInfo = '';
        axios.get(`${SERVICE_URL.tz.list_details}?vid=${this.selectedCaseId}&doc=${this.selectedDocId}`).then((resp) => {
          if(resp.status===200){
            this.htmlInfo = resp.data.data;
          }
        }).catch(function (error) {
          console.log(error);
        });
      },


    },

    created() {

    },

    mounted() {
      this.initCollection();
    },

    computed: {
      currentCollection() {
      }
    }
  }
</script>

<style scoped>
  .el-table .cell {
    white-space: pre-line;
  }
</style>
