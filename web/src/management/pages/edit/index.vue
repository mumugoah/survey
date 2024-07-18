<template>
  <div class="edit-index">
    <button @click="handleSave">点击我</button>
    <!-- <LeftMenu class="left"></LeftMenu> -->
    <div class="right">
      <CommonTemplate style="background-color: #f6f7f9">
        <template #nav>
          <Navbar class="navbar"></Navbar>
        </template>
        <template #body>
          <router-view></router-view>
        </template>
      </CommonTemplate>
    </div>
  </div>
</template>
<script setup lang="ts">
import { onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import 'element-plus/theme-chalk/src/message.scss'

import LeftMenu from '@/management/components/LeftMenu.vue'
import CommonTemplate from './components/CommonTemplate.vue'
import Navbar from './components/ModuleNavbar.vue'

import { initShowLogicEngine } from '@/management/hooks/useShowLogicEngine'
import { showLogicEngine } from '@/management/hooks/useShowLogicEngine'
import buildData  from './modules/contentModule/buildData'
import { saveSurvey } from '@/management/api/survey'


const store = useStore()
const router = useRouter()
const route = useRoute()

onMounted(async () => {
  store.commit('edit/setSurveyId', route.params.id)

  try {
    await store.dispatch('edit/init')
    await initShowLogicEngine(store.state.edit.schema.logicConf.showLogicConf || {})
  } catch (err: any) {
    ElMessage.error(err.message)

    setTimeout(() => {
      router.replace({ name: 'survey' })
    }, 1000)
  }

  window.addEventListener('message', (event) => {
    console.log(event)
    // if (event.data === 'save') {
    //   handleSave()
    // }
  });
})


const updateLogicConf = () => {
  if (
    showLogicEngine.value &&
    showLogicEngine.value.rules &&
    showLogicEngine.value.rules.length !== 0
  ) {
    showLogicEngine.value.validateSchema()
    const showLogicConf = showLogicEngine.value.toJson()
    // 更新逻辑配置
    store.dispatch('edit/changeSchema', { key: 'logicConf', value: { showLogicConf } })
  }
}

const saveData = async () => {
  const saveData = buildData(store.state.edit.schema)

  if (!saveData.surveyId) {
    ElMessage.error('未获取到问卷id')
    return null
  }

  const res = await saveSurvey(saveData)
  return res
}


const handleSave = async () => {
  console.log('点击测试')

  try {
    updateLogicConf()
  } catch (error) {
    ElMessage.error('请检查逻辑配置是否有误')
    return
  }

  try {
    const res: any = await saveData()
    if (res.code === 200) {
      ElMessage.success('保存成功')
    } else {
      ElMessage.error(res.errmsg)
    }
  } catch (error) {
    ElMessage.error('保存问卷失败')
  } 
}

</script>
<style lang="scss" scoped>

.edit-index {
  height: 100%;
  width: 100%;
  overflow: hidden;

  .left {
    position: fixed;
    left: 0;
    top: 0;
    z-index: 100;
  }

  .right {
    min-width: 1160px;
    height: 100%;
    overflow: hidden;
  }

  .navbar {
    border-bottom: 1px solid #e7e9eb;
  }
}
</style>
