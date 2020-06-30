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
        <el-radio-group v-model="collectionRadio" @change="initCollection">
          <el-radio :label="0">旧表</el-radio>
          <el-radio :label="1">新表</el-radio>
        </el-radio-group>
        <el-tooltip class="item" effect="dark" placement="right">
          <div slot="content" v-html="toolTipText">

          </div>
          <i class="el-icon-info"></i>
        </el-tooltip>
      </el-col>
      <el-col :span="4" style="display: flex; align-items: center; justify-content: space-between">
        <el-button type="primary" @click="showInpRecordDetails">查看病历字段</el-button>
        <el-dialog title="病历字段" :visible.sync="showInpRecordDialog" @close="resetInpRecordDialog">
          <el-input
            v-model="searchInpRecord"
            placeholder="输入关键字搜索"
            style="margin-bottom: 20px"
            clearable/>
          <el-table :data="inpRecordDetails.filter(data => !searchInpRecord ||
          data.content.toLowerCase().includes(searchInpRecord.toLowerCase()) ||
          data.title.toLowerCase().includes(searchInpRecord.toLowerCase()))"
                    border
                    height="400"
                    style="width: 100%;margin-bottom: 20px;">
            <el-table-column property="title" label="title" width="150"></el-table-column>
            <el-table-column property="content" label="content"></el-table-column>
          </el-table>
        </el-dialog>
        <el-button type="primary" @click="showFirstPageDetails">查看病案首页字段</el-button>
        <el-dialog title="病历字段" :visible.sync="showFirstPageDialog" @close="resetFirstPageDialog">
          <el-input
            v-model="searchFirstPage"
            placeholder="输入关键字搜索"
            style="margin-bottom: 20px"
            clearable/>
          <el-table :data="firstPageDetails.filter(data => !searchFirstPage ||
          data.content.toLowerCase().includes(searchFirstPage.toLowerCase()) ||
          data.title.toLowerCase().includes(searchFirstPage.toLowerCase()))"
                    border
                    height="400"
                    style="width: 100%;margin-bottom: 20px;">
            <el-table-column property="title" label="title" width="150"></el-table-column>
            <el-table-column property="content" label="content"></el-table-column>
          </el-table>
        </el-dialog>
      </el-col>
    </el-row>
    <el-row>

      <el-col :span="12">

      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12">
        <div v-html="currentInpRecord"></div>
      </el-col>
      <el-col :span="12">
        <div v-html="currentFirstPage"></div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  import axios from 'axios';
  import SERVICE_URL from "../../config/urlConfig";

  export default {
    name: "Emr",
    data() {
      return {
        emrRecords: {"inp_record": [], "first_page": []},
        currentInpRecord: "",
        currentFirstPage: "",
        caseIds: [],
        selectedCaseId: "",
        selectedDocId: "",
        docNames: [],
        toolTipText: "",
        showInpRecordDialog: false,
        showFirstPageDialog: false,
        inpRecordDetails: [],
        firstPageDetails: [],
        collectionRadio: 0,
        searchInpRecord: "",
        searchFirstPage: "",
      }
    },

    methods: {

      initCollection(){
        this.emrRecords = {"inp_record": [], "first_page": ""};
        this.currentFirstPage = "";
        this.currentInpRecord = "";
        this.selectedDocId = "";
        this.docNames = [];
        this.toolTipText = "";
        this.caseIds = [];
        axios.post(SERVICE_URL.emr.list_emr, {
          "collection_name": this.currentCollection
        }).then((response) => {
          if (response.status === 200) {
            for (let d of response.data.data) {
              this.caseIds.push(d);
            }
          }
        }).catch(function (error) {
          console.log(error);
        });
      },

      get_emr() {
        this.emrRecords = {"inp_record": [], "first_page": ""};
        this.currentFirstPage = "";
        this.currentInpRecord = "";
        this.selectedDocId = "";
        this.docNames = [];
        this.toolTipText = "";
        axios.get(`${SERVICE_URL.emr.get_emr}?caseId=${this.selectedCaseId}&collection_name=${this.currentCollection}`).then((response) => {
          if (response.status === 200 && response.data.code === 20000) {
            this.emrRecords = response.data.data;
            this.currentFirstPage = this.emrRecords["first_page"].length > 0 ? this.emrRecords["first_page"][0]["htmlContent"] : "";
            for (let i in this.emrRecords["inp_record"]) {
              this.docNames.push({
                "key": this.emrRecords["inp_record"][i].title,
                "value": i,
              });
            }
            this.selectedDocId = this.docNames[0].value;
            this.currentInpRecord = this.emrRecords["inp_record"].length > 0 ? this.emrRecords["inp_record"][0]["htmlContent"] : "";
          }
        })
          .catch(function (error) {
            console.log(error);
          });
        axios.get(`${SERVICE_URL.emr.get_basic_info}?caseId=${this.selectedCaseId}&collection_name=${this.currentCollection}`).then((response) => {
          if (response.status === 200 && response.data.code === 20000) {
            for (let i in response.data.data) {
              this.toolTipText += `&nbsp;&nbsp;${i}:&nbsp;&nbsp;${response.data.data[i]} <br/>`;
            }
          }
        })
      },

      get_doc() {
        this.currentInpRecord = this.emrRecords.inp_record[this.selectedDocId].htmlContent;
      },

      showInpRecordDetails() {
        this.showInpRecordDialog = true;
        axios.get(`${SERVICE_URL.emr.get_fields}?caseId=${this.selectedCaseId}&docName=${this.docNames[this.selectedDocId].key}&collection_name=${this.currentCollection}`).then((response) => {
          if (response.status === 200 && response.data.code === 20000) {
            this.inpRecordDetails = response.data.data;
          }
        });
      },

      showFirstPageDetails() {
        this.showFirstPageDialog = true;
        axios.get(`${SERVICE_URL.emr.get_fields}?caseId=${this.selectedCaseId}&docName=病案首页&collection_name=${this.currentCollection}`).then((response) => {
          if (response.status === 200 && response.data.code === 20000) {
            this.firstPageDetails = response.data.data;
          }
        });
      },

      resetInpRecordDialog(){
        this.searchInpRecord = "";
      },

      resetFirstPageDialog(){
        this.searchFirstPage = "";
      },

    },

    created() {

    },

    mounted() {
      this.initCollection();
    },

    computed: {
      currentCollection() {
        return ["emr", "emr20"][this.collectionRadio];
      }
    }
  }
</script>

<style scoped>
  .el-table .cell {
    white-space: pre-line;
  }
</style>
