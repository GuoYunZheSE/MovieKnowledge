<template>
  <el-card class="container">
    <div slot="header">
      <span class="title">Movie Query</span>
    </div>
    <div class="filter-container">
      <el-input v-model="listQuery.movieTitle" placeholder="Movie Title" style="width: 150px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <!--      <el-date-picker v-model="listQuery.rate_date" type="datetime" style="width: 150px;" value-format="yyyy-MM-dd" class="filter-item" placeholder="公布" />-->
      <el-select v-model="listQuery.genre" style="width: 140px" placeholder="Genre" class="filter-item" @change="handleFilter">
        <el-option v-for="item in genreOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
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
      <el-table-column label="Title" prop="movieTitle" min-width="45px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.movieTitle }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Release Date" prop="movieReleaseDate" min-width="30px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.movieReleaseDate }}</span>
        </template>
      </el-table-column>collect_grade
      <el-table-column label="Rating" prop="movieRating" min-width="30px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.movieRating }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Introduction" show-overflow-tooltip prop="movieIntroduction" min-width="120px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.movieIntroduction }}</span>
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
import { QueryMovie } from '@/api';

export default {
  name: 'QueryMovie',
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
        sort: '+movieReleaseDate',
        movieTitle: undefined,
        movieReleaseDate: undefined,
        movieIntroduction: undefined,
        genre: undefined,
      },
      sortOptions: [
        { label: 'From New to Old', key: '-movieReleaseDate' },
        { label: 'From Old to New', key: '+movieReleaseDate'},
        { label: 'Rating Ascending', key: '+movieRating'},
        { label: 'Rating Descending', key: '-movieRating'}
        ],
      genreOptions: [
        { label: 'All Genre', key: '' },
        { label: 'Adventure', key: 'Adventure' },
        { label: 'Fantasy', key: 'Fantasy' },
        { label: 'Animation', key: 'Animation' },
        { label: 'Drama', key: 'Drama' },
        { label: 'Thriller', key: 'Thriller' },
        { label: 'Action', key: 'Action' },
        { label: 'Comedy', key: 'Comedy' },
        { label: 'History', key: 'History' },
        { label: 'Western', key: 'Western' },
        { label: 'Horror', key: 'Horror' },
        { label: 'Crime', key: 'Crime' },
        { label: 'Documentary', key: 'Documentary' },
        { label: 'Science Fiction', key: 'Science Fiction' },
        { label: 'Mystery', key: 'Mystery' },
        { label: 'Music', key: 'Music' },
        { label: 'Romance', key: 'Romance' },
        { label: 'Family', key: 'Family' },
        { label: 'War', key: 'War' },
        { label: 'TV Movie', key: 'TV Movie' },
      ],
    }
  },
  created() {
    this.getList();
  },
  methods: {
    getList() {
      this.listLoading = true;
      QueryMovie(this.listQuery).then((response) => {
        this.list = response.data.items;
        this.total = response.data.total;
        this.listLoading = false;
      });
    },
    handleFilter() {
      this.listQuery.page = 1;
      this.getList();
    },
    sortChange(data) {
      const { prop, order } = data;
      if (prop === 'movieReleaseDate') {
        this.sortByID(order);
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+movieReleaseDate';
      } else {
        this.listQuery.sort = '-movieReleaseDate';
      }
      this.handleFilter();
    },
    getSortClass(key) {
      const { sort } = this.listQuery;
      return sort === `+${key}` ? 'ascending' : 'descending';
    },
    tabRowClassName({ row, rowIndex }) {
      const index = rowIndex + 1;
      // eslint-disable-next-line eqeqeq
      if (index % 2 === 0) {
        return 'warning-row';
      }
    },
  },
};
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
