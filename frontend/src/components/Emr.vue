<template>
  <div>
    <el-row>
      <el-col :span="6" style="display: flex; align-items: center; justify-content: space-between">
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
        <el-tooltip class="item" effect="dark" placement="right">
          <div slot="content" v-html="toolTipText">

          </div>
          <i class="el-icon-info"></i>
        </el-tooltip>
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
      }
    },

    methods: {

      get_emr() {
        this.emrRecords = {"inp_record": [], "first_page": ""};
        this.currentFirstPage = "";
        this.currentInpRecord = "";
        this.selectedDocId = "";
        this.docNames = [];
        this.toolTipText = "";
        axios.get(SERVICE_URL.emr.get_emr + "?caseId=" + this.selectedCaseId).then((response) => {
          if (response.status === 200 && response.data.code === 20000) {
            this.emrRecords = response.data.data;
            this.currentFirstPage = this.emrRecords["first_page"].length > 0 ? this.emrRecords["first_page"][0]["content"] : "";
            for (let i of this.emrRecords["inp_record"]) {
              this.docNames.push({
                "key": i["title"],
                "value": i["docId"],
              });
            }
            this.selectedDocId = this.docNames[0].value;
            this.currentInpRecord = this.emrRecords["inp_record"].length > 0 ? this.emrRecords["inp_record"][0]["content"] : "";
          }
        })
          .catch(function (error) {
            console.log(error);
          });
        axios.get(SERVICE_URL.emr.get_basic_info + "?caseId=" + this.selectedCaseId).then((response) => {
          if (response.status === 200 && response.data.code === 20000) {
            for (let i in response.data.data){
              this.toolTipText += `&nbsp;&nbsp;${i}:&nbsp;&nbsp;${response.data.data[i]} <br/>`;
            }
          }
        })
      },

      get_doc() {
        this.currentInpRecord = "";
        for (let i of this.emrRecords.inp_record) {
          if (i["docId"] === this.selectedDocId) {
            this.currentInpRecord = i.content;
          }
        }
      },

    },

    created() {

    },

    mounted() {
      axios.post(SERVICE_URL.emr.list_emr, {
        "start": 0,
        "size": 370
      }).then((response) => {
        if (response.status === 200) {
          for (let d of response.data.data) {
            this.caseIds.push(d);
          }
        }
      })
        .catch(function (error) {
          console.log(error);
        });
    },

    computed: {}
  }
</script>

<style scoped>
  .el-table .cell {
    white-space: pre-line;
  }
</style>
