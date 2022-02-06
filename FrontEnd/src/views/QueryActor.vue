<template>
  <el-card class="container">
    <div slot="header">
      <span class="title">Actor Query</span>
    </div>
    <div class="filter-container">
      <el-input v-model="listQuery.personEnglishName" placeholder="Actor Name" style="width: 150px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <!--      <el-date-picker v-model="listQuery.rate_date" type="datetime" style="width: 150px;" value-format="yyyy-MM-dd" class="filter-item" placeholder="公布" />-->
      <el-select v-model="listQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
    </div>
    <el-table
      :key="tableKey"
      v-loading="listLoading"
      height="250"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      :row-class-name="tabRowClassName"
      :header-cell-style="{background:'#5eacfd',color:'#fefefe'}"
      @sort-change="sortChange"
    >
      <el-table-column label="ID" prop="id" align="center" width="80">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Actor Name" prop="personEnglishName" min-width="45px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.personEnglishName }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Actor Birthday" prop="PersonBirthDay" min-width="30px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.PersonBirthDay }}</span>
        </template>
      </el-table-column>collect_grade
      <el-table-column label="Actor DeathDay" prop="personDeathDay" min-width="30px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.personDeathDay }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Actor BirthPlace" prop="personBirthPlace" min-width="30px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.personBirthPlace }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Actor Biography" show-overflow-tooltip prop="personBiography" min-width="120px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.personBiography }}</span>
        </template>
      </el-table-column>
      <!--      <el-table-column label="公布日期" prop="rate_date" sortable="custom" min-width="20px" align="center" :class-name="getSortClass('rate_date')">-->
      <!--        <template slot-scope="{row}">-->
      <!--          <span>{{ row.publish_date }}</span>-->
      <!--        </template>-->
      <!--      </el-table-column>-->
    </el-table>
    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

  </el-card>
</template>
<script>
import waves from '@/waves/waves';// waves directive
import Pagination from '@/Pagination/index.vue'; // secondary package based on el-pagination
import { QuuryActor } from '@/api';

export default {
  name: 'Query',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        sort: '+PersonBirthDay',
        personEnglishName: undefined,
        personBiography: undefined,
        PersonBirthDay: undefined,
        personBirthPlace: undefined,
        personDirthDay: undefined
      },
      sortOptions: [{ label: 'From Younger to Older', key: '-PersonBirthDay' }, { label: 'From Older to Younger', key: '+PersonBirthDay' }],
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      QuuryActor(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'PersonBirthDay') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+PersonBirthDay'
      } else {
        this.listQuery.sort = '-PersonBirthDay'
      }
      this.handleFilter()
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    },
    tabRowClassName({ row, rowIndex }) {
      const index = rowIndex + 1
      // eslint-disable-next-line eqeqeq
      if (index % 2 === 0) {
        return 'warning-row'
      }
    }
  }
}
</script>
<style>
.el-table .warning-row{
  background:#F3F9FF
}
.el-table--enable-row-hover .el-table__body tr:hover > td {
  background-color: #cff6da;
}
.el-table--striped .el-table__body tr.el-table__row--striped.current-row td, .el-table__body tr.current-row>td {
  color: #000000;
  background-color: #8febb8 !important;
}
.el-table__header tr,
.el-table__header th {
  padding: 0;
  height: 20px;
}

</style>
