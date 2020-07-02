<template>
  <div>
    <el-row :gutter="40">
      <el-col :span="8" style="display: flex; align-items: center; justify-content: space-between">
        <el-input
          v-model="searchCaseId"
          placeholder="输入病历号"
          clearable>
          <el-button slot="append" icon="el-icon-search" @click="getCase"></el-button>
        </el-input>
      </el-col>
      <el-col :span="8" style="display: flex; align-items: center; justify-content: space-between;">
        <el-select v-model="selectFirstDoc"
                   placeholder="请选择文档"
                   @change="get_first_doc"
                   filterable>
          <el-option
            v-for="(item, index) in docNames"
            :key="index"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
        <el-select v-model="selectSecondDoc"
                   placeholder="请选择文档"
                   @change="get_second_doc"
                   filterable>
          <el-option
            v-for="(item, index) in docNames"
            :key="index"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12">
        <div v-html="currentFirstDoc"></div>
      </el-col>
      <el-col :span="12">
        <div v-html="currentSecondDoc"></div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  import axios from 'axios';
  import SERVICE_URL from "../../config/urlConfig";

  export default {
    name: "Emrx",
    data() {
      return {
        emrRecords: [],
        currentFirstDoc: "",
        currentSecondDoc: "",
        caseIds: [],
        docNames:[],
        selectedCaseId: "",
        selectedDocId: "",
        inpRecordDetails: [],
        firstPageDetails: [],
        collectionRadio: 0,
        searchCaseId: "",
        selectFirstDoc: "",
        firstDocName: [],
        selectSecondDoc: "",
        secondDocName: [],
      }
    },

    methods: {
      getCase() {
        let _this = this;
        _this.emrRecords = [];
        _this.docNames = [];
        _this.currentFirstDoc = "";
        _this.currentSecondDoc = "";
        axios.get(`${SERVICE_URL.emr.get_emrx}?caseId=${_this.searchCaseId}`).then((response) => {
          if (response.status === 200 && response.data.code === 20000) {
            _this.emrRecords = response.data.data;
            for (let i of _this.emrRecords) {
              _this.docNames.push(i.title);
            }
            _this.selectFirstDoc = _this.docNames[0];
            _this.get_first_doc();
            _this.selectSecondDoc = _this.docNames[1];
            _this.get_second_doc();
          }
        }).catch(function (error) {
            console.log(error);
          });
      },

      get_first_doc(){
        let tmp = this.emrRecords.filter((data)=>{
          if (data.title === this.selectFirstDoc) return data;
        });
        this.currentFirstDoc = tmp.length > 0 ? tmp[0].htmlContent : "";
      },

      get_second_doc(){
        let tmp = this.emrRecords.filter((data)=>{
          if (data.title === this.selectSecondDoc) return data;
        });
        this.currentSecondDoc = tmp.length > 0 ? tmp[0].htmlContent : "";
      }
    },

    created() {

    },

    mounted() {

    },

    computed: {}
  }
</script>

<style scoped>
  .el-table .cell {
    white-space: pre-line;
  }
</style>
