<template>
  <div style="height: 100%">
    <el-row :gutter="20">
      <el-col :span="8" style="display: flex; align-items: center; justify-content: space-between">
        <el-select v-model="selectedCaseId"
                   placeholder="请选择caseId"
                   @change="getDetails"
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
                   filterable>
          <el-option
            v-for="item in docNames"
            :key="item.value"
            :label="item.key"
            :value="item.value">
          </el-option>
        </el-select>
        <i class="el-icon-delete" @click="deleteAllData"></i>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <div v-html="showEmr" style="height: 600px; overflow: auto;"></div>
      </el-col>
      <el-col :span="12">
        <el-table
          ref="filterTable"
          :data="qcResults"
          height="600"
          border
          style="width: 100%">
          <el-table-column
            prop="check_id"
            label="check_id"
            width="120">
          </el-table-column>
          <el-table-column
            prop="code"
            label="code"
            width="120"
            :filters="[{text: 'GOOD', value: 1}, {text: 'BAD', value: 2}, {text: 'WARNING', value: 3},
            {text: 'LACK', value: 4}, {text: 'WRONG_TYPE', value: 5}, {text: 'NOT_YET', value: 6},
            {text: 'SKIP', value: 7}, {text: 'ERROR', value: 8}, {text: 'LACK_DOC', value: 9}]"
            :filter-method="filterHandler">
          </el-table-column>
          <el-table-column
            prop="doc_id"
            label="doc_id"
            width="120">
          </el-table-column>
          <el-table-column
            prop="message"
            label="message">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="100">
            <template slot-scope="scope">
              <el-button @click="reviewDocument(scope.row)" type="text" size="small">查看相关文档</el-button>
            </template>
          </el-table-column>
          <el-table-column
            prop="doctor_result"
            label="医生判断"
            width="100"
            :filters="[{ text: '错', value: '错' }, { text: '对', value: '对'}, { text: '无', value: '无'}]"
            :filter-method="filterDoctorResult">
            <template slot-scope="scope">
              <el-tag
                :type="changeStatusView(scope.row.doctor_result)">
                {{scope.row.doctor_result}}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
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
        emrRecords: [],
        basicInfo: {},
        caseIds: [],
        selectedCaseId: "",
        selectedDocId: "",
        showEmr: "",
        qcResults: [],
        docNames: [],
        toolTipText: "",
      }
    },

    methods: {

      initCollection() {
        this.emrRecords = [];
        this.basicInfo = {};
        this.selectedDocId = "";
        this.docNames = [];
        this.toolTipText = "";
        this.caseIds = [];
        this.qcResults = [];
        axios.get(`${SERVICE_URL.testCases.list_caseId}?hospital=lishui`).then((response) => {
          if (response.status === 200) {
            for (let d of response.data.data) {
              this.caseIds.push(d);
            }
          }
        }).catch(function (error) {
          console.log(error);
        });
      },

      getDetails() {
        this.getEmr();
        this.getQcResults();
      },

      getEmr() {
        this.emrRecords = [];
        this.basicInfo = {};
        this.selectedDocId = "";
        this.docNames = [];
        this.toolTipText = "";
        this.qcResults = [];
        axios.get(`${SERVICE_URL.testCases.get_emr}?caseId=${this.selectedCaseId}`).then((response) => {
          if (response.status === 200 && response.data.code === 20000) {
            this.emrRecords = response.data.data.emr;
            this.basicInfo = response.data.data.basicInfo;
            for (let i of this.emrRecords) {
              this.docNames.push({
                "key": i.documentName,
                "value": i.docId,
              });
            }
            this.selectedDocId = this.docNames[0].value;
          }
        })
          .catch(function (error) {
            console.log(error);
          });
      },

      getDoc() {
        this.showEmr = "";
        for (let i of this.emrRecords) {
          if (i.docId === this.selectedDocId) {
            this.showEmr = i.htmlContent;
          }
        }
      },

      getQcResults() {
        axios.get(`${SERVICE_URL.testCases.get_qc}?caseId=${this.selectedCaseId}`).then((response) => {
          if (response.status === 200 && response.data.code === 20000) {
            this.qcResults = response.data.data;
          }
        })
          .catch(function (error) {
            console.log(error);
          });

      },

      filterHandler(value, row, column) {
        const property = column['property'];
        return row[property] === value;
      },

      reviewDocument(row) {
        let docId = row.doc_id;
        if (docId.length > 0) {
          this.selectedDocId = docId[0];
          this.getDoc();
        }
      },

      deleteAllData() {
        this.$confirm('此操作将永久删除数据库, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          axios.post(SERVICE_URL.testCases.delete_qcs, {}).then((response) => {
            if (response.status === 200 && response.data.code === 20000) {
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
            }
          }).catch(function (error) {
            console.log(error);
            this.$message({
              type: 'info',
              message: '已取消删除'
            })
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },

      filterDoctorResult(value, row) {
        return row.doctor_result === value;
      },

      changeStatusView(status){
        if (status==='对'){
          return 'warning'
        }else if(status==='错'){
          return 'success'
        }else{
          return 'info'
        }
      }

    },

    created() {

    },

    mounted() {
      this.initCollection();
    },

    watch: {
      selectedDocId() {
        this.getDoc();
      }
    },

    computed: {}
  }
</script>

<style>
  .el-table .cell {
    white-space: pre-line;
  }

  .el-row {
    margin-bottom: 20px;
  }

  .el-row:last-child {
    margin-bottom: 0;
  }

  p, span {
    line-height: 24px !important;
  }
</style>
