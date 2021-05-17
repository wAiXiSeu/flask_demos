<template>
  <div style="height: 100%">
    <el-row :gutter="20">
      <el-col :span="8" style="display: flex; align-items: center; justify-content: space-between">
        <el-select v-model="selectedCaseId"
                   placeholder="请选择caseId"
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
        <a class="el-icon-download" :href="SERVICE_URL.testCases.download_qcs"></a>
        <el-button type="text" @click="showTestCaseTable = true">查看测试用例</el-button>
        <el-dialog title="测试用例" :visible.sync="showTestCaseTable">
          <el-col :span="12" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px">
            <el-input
              placeholder="请输入内容"
              prefix-icon="el-icon-search"
              v-model="testCaseKeyWord"
              @keyup.enter.native="searchTestCase">
            </el-input>
            <el-checkbox v-model="onlyConflictCase" style="margin-left: 10%">只显示冲突项</el-checkbox>
          </el-col>

          <el-table ref="filterTable" border height="600"
                    :data="testCaseTableData"
                    :row-class-name="testCaseStatus"
                    :default-sort = "{prop: 'qc_id', order: 'ascending'}">
            <el-table-column property="caseId" label="caseId" width="150">
              <template slot-scope="{row}">
                <el-link @click="selectedCaseId = row.caseId; showTestCaseTable=false">{{row.caseId}}</el-link>
              </template>
            </el-table-column>
            <el-table-column property="qc_id" label="质控点编号" width="200"></el-table-column>
            <el-table-column property="qc_name" label="质控点名称"></el-table-column>
            <el-table-column property="doctor_result" label="医生判断"></el-table-column>
            <el-table-column property="errorReason" label="错误信息"></el-table-column>
            <el-table-column property="code" label="质控结果"></el-table-column>
          </el-table>
          <el-pagination
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-size="20"
            layout="total, prev, pager, next"
            :total="testCaseFilterData.length">
          </el-pagination>
        </el-dialog>
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
        showTestCaseTable: false,
        testCaseKeyWord: '',
        testCaseTotalData: [], // 所有用例数据
        testCaseTableData: [], // 表格中展示的一页数据
        testCaseFilterData: [], // 筛选的用例数据
        currentPage: 1,
        onlyConflictCase: false, // 是否只显示质控结果和医生判断不一致的点
        SERVICE_URL,
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
          if (response.status === 200 && response.data.code === 20000) {
            for (let d of response.data.data) {
              this.caseIds.push(d);
            }
          }
        }).catch(function (error) {
          console.log(error);
        });
        this.getDoctorResults();
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
            this.showEmr = i.htmlContent instanceof Object ? i.htmlContent : i.htmlContent.replace('background-color:white;', '');
          }
        }
      },

      getQcResults() {
        axios.get(`${SERVICE_URL.testCases.get_qc}?caseId=${this.selectedCaseId}&pages=${this.currentPage}
        &page_size=20`).then((response) => {
          if (response.status === 200 && response.data.code === 20000) {
            this.qcResults = response.data.data;
          }
        })
          .catch(function (error) {
            console.log(error);
          });

      },

      getDoctorResults() {
        this.currentPage = 1;
        axios.get(`${SERVICE_URL.testCases.doctor_result}`)
          .then((response) => {
            if (response.status === 200 && response.data.code === 20000) {
              this.testCaseTotalData = response.data.data;
              this.testCaseFilterData = this.testCaseTotalData;
              this.testCaseTableData = this.testCaseFilterData.slice(
                20 * (this.currentPage-1), 20* this.currentPage
              );
            }
          }).catch(function (error) {
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

      changeStatusView(status) {
        if (status === '对') {
          return 'warning'
        } else if (status === '错') {
          return 'success'
        } else {
          return 'info'
        }
      },

      handleCurrentChange(val) {
        //修改当前页
        this.currentPage = val;
        this.testCaseTableData = this.testCaseFilterData.slice(20 * (this.currentPage-1),20* this.currentPage);
      },

      searchTestCase() {
        this.currentPage = 1;
        this.testCaseFilterData = this.testCaseTotalData.filter(data => !this.testCaseKeyWord ||
          data.qc_id.toLowerCase().includes(this.testCaseKeyWord.toLowerCase()));
        this.testCaseTableData = this.testCaseFilterData.slice(20 * (this.currentPage-1),20* this.currentPage);
      },

      testCaseStatus({row, rowIndex}) {
        if (row.code === '') {
          return ''
        }
        if ((row.code !== "2" && row.doctor_result === '错')
          || (row.code !== "1" && row.doctor_result === '对')) {
          return 'warning-row';
        }
        return '';
      },

    },

    created() {

    },

    mounted() {
      this.initCollection();
    },

    watch: {
      selectedDocId() {
        this.getDoc();
      },
      selectedCaseId() {
        this.getDetails();
      },
      onlyConflictCase() {
        this.currentPage = 1;
        if (this.onlyConflictCase) {
          this.testCaseFilterData = this.testCaseTotalData.filter(data => data.code !== "" &&
            ((data.code !== "2" && data.doctor_result === "错") || (data.code !== "1" && data.doctor_result === "对")));
          this.testCaseTableData = this.testCaseFilterData.slice(20 * (this.currentPage-1),20* this.currentPage);
        }else{
          this.searchTestCase();
        }
      },
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

  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }

  p, span {
    line-height: 24px !important;
  }
</style>
