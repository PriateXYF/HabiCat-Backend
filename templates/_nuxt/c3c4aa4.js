(window.webpackJsonp=window.webpackJsonp||[]).push([[11],{394:function(t,e,o){"use strict";o.d(e,"a",(function(){return c}));var n=o(130);var r=o(180),l=o(89);function c(t){return function(t){if(Array.isArray(t))return Object(n.a)(t)}(t)||Object(r.a)(t)||Object(l.a)(t)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}},408:function(t,e,o){var content=o(422);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,o(46).default)("1a3edd5a",content,!0,{sourceMap:!1})},421:function(t,e,o){"use strict";o(408)},422:function(t,e,o){var n=o(45)(!1);n.push([t.i,'.reading-more-text{margin:13px}.card-book-name{font-size:15px;font-family:"宋体","Arial","Microsoft YaHei","黑体",sans-serif}.book-page-input{width:64px}.page-word .el-form-item__label-wrap{margin-left:0!important}input::-webkit-inner-spin-button,input::-webkit-outer-spin-button{-webkit-appearance:none!important;margin:0}.book-button{background:transparent}.book-button:hover{padding-left:30px;padding-right:30px;transition:padding .3s}.book-button:focus,.book-button:hover{background-color:transparent}.reading-input{height:15px}.bbdc-tag{font-size:15px}.bbdc-more-text{margin:34px}.bbdc-info{font-size:20px;line-height:20px}.bbdc-page::-webkit-scrollbar{width:0!important}.bbdc-page{max-height:1000px;height:auto;-ms-overflow-style:none;overflow:-moz-scrollbars-none}.bbdc-item{font-size:20px;display:flex;align-items:center;justify-content:center;height:30px}@media screen and (max-width:560px){.bbdc-item{font-size:15px}}.bbdc-item-title{font-size:30px;margin-top:5px;display:flex;align-items:center;justify-content:center;height:50px}.bbdc-hr{margin:30px 20%}',""]),t.exports=n},432:function(t,e,o){"use strict";o.r(e);var n=o(394),r=(o(87),o(88),{data:function(){return{isMost:!1,page:0,datas:[],isLoading:!1,form:{bookname:"",bookpage:0},display:{xs:24,sm:12,md:8,lg:6,xl:4}}},methods:{getData:function(){var t=this;this.$axios.$post("api/reading",{page:this.page}).then((function(e){t.datas=[].concat(Object(n.a)(t.datas),Object(n.a)(e)),e.length<10&&(t.isMost=!0)}))},load:function(){this.page+=1,this.getData()},parseDate:function(t){var e=new Date(t);return e.getMonth()+1+"月"+e.getDate()+"日 "+e.getHours()+":"+(e.getMinutes()<10?"0"+e.getMinutes():e.getMinutes())},getDiff:function(t,e){var o=t+"->"+e;return Math.abs(t-e)<.1&&(o=""+e),o},doReadingExport:function(){if(this.datas[0]&&this.form.bookname==this.datas[0].bookName){var t=this.datas[0].bookPage;if(this.form.bookpage-t>100)return void this.$message("你读太多书啦，一次不要超过100页哦！");if(this.form.bookpage-t<=0)return void this.$message("你还没有读书哦！")}var e=this;this.isLoading=!0,this.$message("请求已发送，正在检测当前读书状态!"),this.$axios.$post("api/doReading",{bookName:e.form.bookname,bookPage:parseInt(e.form.bookpage)}).then((function(t){e.$message(t.msg),setTimeout((function(){e.$router.push({path:"reload",query:{reload:"reading"}})}),2e3)})).catch((function(t){e.$message("状态异常，请稍后再试!"),e.isLoading=!1}))},changeDisplay:function(){24==this.display.xl?this.display={xs:24,sm:12,md:8,lg:6,xl:4}:this.display={xs:24,sm:24,md:24,lg:24,xl:24}},shortName:function(t){var e=t;return t.length>10&&(e=t.substr(0,4)+"..."+t.substr(t.length-3,3)),e},setForm:function(t){this.form.bookpage=t.bookPage,this.form.bookname=t.bookName}},mounted:function(){this.datas[0]&&(this.form.bookname=this.datas[0].bookName),this.datas[0]&&(this.form.bookpage=this.datas[0].bookPage)},asyncData:function(content){return content.$axios.$post("api/reading",{page:0}).then((function(t){return console.log(t),{datas:t}}))},computed:{cardStyle:function(){return 24==this.display.xl?{backgroundColor:"transparent",borderTop:"0px",borderLeft:"0px",borderRight:"0px",boxShadow:"0 0 0 0 !important",cursor:"auto"}:{}}}}),l=(o(421),o(55)),component=Object(l.a)(r,(function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("el-container",[o("el-header",[o("el-row",{staticClass:"head-list"},[o("div",{staticClass:"head-list-left"},[o("nuxt-link",{attrs:{to:"/page"}},[o("el-button",{staticClass:"icon-button",attrs:{icon:"el-icon-s-home"}})],1)],1),t._v(" "),o("div",{staticClass:"head-list-right"},[o("el-button",{staticClass:"icon-button",attrs:{icon:"el-icon-s-operation"},on:{click:t.changeDisplay}}),t._v(" "),o("el-button",{directives:[{name:"show",rawName:"v-show",value:!t.isLoading,expression:"!isLoading"}],staticClass:"icon-button",attrs:{icon:"el-icon-thumb"},on:{click:t.doReadingExport}}),t._v(" "),o("el-button",{directives:[{name:"show",rawName:"v-show",value:t.isLoading,expression:"isLoading"}],staticClass:"icon-button",attrs:{icon:"el-icon-loading"}})],1)])],1),t._v(" "),o("el-main",[o("el-divider",{staticClass:"card-divider",attrs:{"content-position":"left"}},[t._v("读书记录")]),t._v(" "),o("el-row",{staticClass:"row-bg",attrs:{type:"flex",justify:"center"}},[o("el-form",{attrs:{inline:!0,"label-position":"right","label-width":"auto",model:t.form}},[o("el-form-item",{attrs:{label:"现在在读"}},[o("el-input",{staticClass:"book-input",model:{value:t.form.bookname,callback:function(e){t.$set(t.form,"bookname",e)},expression:"form.bookname"}})],1),t._v(" "),o("el-form-item",{attrs:{label:"已经读到"}},[o("el-input",{staticClass:"book-input book-page-input",attrs:{type:"number"},model:{value:t.form.bookpage,callback:function(e){t.$set(t.form,"bookpage",e)},expression:"form.bookpage"}})],1),t._v(" "),o("el-form-item",{staticClass:"page-word",attrs:{label:"页"}})],1)],1),t._v(" "),o("el-row",{staticClass:"allcard"},[t._l(t.datas,(function(e,n){return o("el-col",{key:n,attrs:{xs:t.display.xs,sm:t.display.sm,md:t.display.md,lg:t.display.lg,xl:t.display.xl}},[o("el-card",{staticClass:"indexcontainer card",style:t.cardStyle,nativeOn:{click:function(o){return t.setForm(e)}}},[o("div",[o("span",[o("el-tag",{staticClass:"github-tag card-book-name",attrs:{effect:"dark"}},[t._v(" "+t._s(t.shortName(e.bookName))+" \n                ")]),t._v(" "),o("el-tag",{staticClass:"github-tag",attrs:{effect:"dark"}},[t._v("  "+t._s(e.bookPage)+" \n                ")])],1),t._v(" "),o("div",{staticClass:"bottom clearfix"},[o("div",{staticClass:"desc"},[t._v(t._s(t.parseDate(e.date)))])]),t._v(" "),o("div",{staticClass:"bottom clearfix"},[o("div",{staticClass:"bbdc-info"},[t._v(t._s(e.info))])])])])],1)})),t._v(" "),o("el-col",{directives:[{name:"show",rawName:"v-show",value:!t.isMost,expression:"!isMost"}],attrs:{xs:t.display.xs,sm:t.display.sm,md:t.display.md,lg:t.display.lg,xl:t.display.xl}},[o("el-card",{staticClass:"card",nativeOn:{click:function(e){return t.load.apply(null,arguments)}}},[o("div",{staticClass:"reading-more-text",staticStyle:{padding:"14px"}},[o("span",[t._v("加载更多")]),t._v(" "),o("div",{staticClass:"bottom clearfix"},[o("div",{staticClass:"desc"},[t._v("More")])])])])],1)],2)],1),t._v(" "),o("el-footer")],1)}),[],!1,null,null,null);e.default=component.exports}}]);