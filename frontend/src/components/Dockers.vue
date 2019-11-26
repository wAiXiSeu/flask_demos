<template>
  <el-row>
    <el-row>
      <el-col :span="6">
        <el-form :inline="true" class="demo-form-inline">
          <el-form-item label="Tags">
            <el-input v-model="imageTag" placeholder="镜像名称"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="queryImages(imageTag)">查询</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-table
          ref="multipleTable"
          border
          height="600"
          :data="tableData"
          tooltip-effect="dark"
          style="width: 100%">
          <el-table-column
            type="index"
            label="index"
            width="60">
          </el-table-column>
          <el-table-column
            prop="id"
            label="Image ID"
            width="200">
          </el-table-column>
          <el-table-column
            label="tags"
            width="200">
            <template slot-scope="scope">{{scope.row.tags.join("\n")}}</template>
          </el-table-column>
          <el-table-column
            prop="container"
            label="container"
            width="200">
          </el-table-column>
          <el-table-column
            label="created"
            width="200">
            <template slot-scope="scope">{{scope.row.created}}</template>
          </el-table-column>
          <el-table-column
            prop="since"
            label="age(天)"
            width="200">
          </el-table-column>
          <el-table-column
            prop="size"
            label="size(GB)"
            width="200">
          </el-table-column>
          <el-table-column
            label="操作">
            <template slot-scope="scope">
              <el-button @click="deleteImage(scope.row.id, scope.$index)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
  </el-row>
</template>
<script>
  import axios from 'axios';
  import SERVICE_URL from "../../config/urlConfig";

  export default {
    name: "Dockers",
    data() {
      return {
        tableData: [],
        dockerImages: [],
        multipleSelection: [],
        imageTag: ""
      }
    },

    methods: {
      get_docker_images() {
        axios.get(SERVICE_URL.dockers.list_images)
          .then((response) => {
            if (response.data.code === 0) {
              this.dockerImages = response.data.data;
              this.tableData = response.data.data;
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      },
      deleteImage(imageId, index) {
        this.$confirm('此操作将永久删除该镜像, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          axios.post(SERVICE_URL.dockers.delete_images, {
            "imageId": imageId
          }).then((response) => {
            if (response.data.code === 0) {
              // 重新渲染表格
              this.dockerImages.splice(index, 1);
              this.tableData.splice(index, 1);
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
            } else {
              this.$message({
                type: "warn",
                message: response.data.message
              });
            }
          })
            .catch(function (error) {
              console.log(error);
            });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });

      },

      queryImages(tag) {
        this.tableData = this.dockerImages.filter((item, key) => {
          let flag = false;
          item.tags.map(function (it) {
            if (it.search(tag.trim()) !== -1) {
              flag = true
            }
          });
          return flag;
        });
      },
    },

    created() {
      this.get_docker_images();
    }
  }
</script>

<style scoped>
  .el-table .cell {
    white-space: pre-line;
  }
</style>
