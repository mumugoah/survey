export const menuItems = {
  textarea: {
    type: 'textarea',
    snapshot: '/imgs/question-type-snapshot/11iAo3ca0u1657702225416.webp',
    path: 'TextareaModule',
    icon: 'tixing-duohangshuru',
    title: '输入题'
  },
  radio: {
    type: 'radio',
    snapshot: '/imgs/question-type-snapshot/TgeRDfURJZ1657702220602.webp',
    icon: 'tixing-danxuan',
    path: 'RadioModule',
    title: '单选题'
  },
  checkbox: {
    type: 'checkbox',
    path: 'CheckboxModule',
    snapshot: '/imgs/question-type-snapshot/Md2YmzBBpV1657702223744.webp',
    icon: 'tixing-duoxuan',
    title: '多选题'
  },
  'radio-nps': {
    type: 'radio-nps',
    path: 'NpsModule',
    snapshot: '/imgs/question-type-snapshot/radio-nps.webp',
    icon: 'NPSpingfen',
    title: '评分题'
  },

}

const menuGroup = [
  {
    title: '输入题型',
    questionList: ['textarea']
  },
  {
    title: '选择题型',
    questionList: ['radio', 'checkbox', 'radio-nps']
  }
]

const menu = menuGroup.map((group) => {
  group.questionList = group.questionList.map((question) => menuItems[question])
  return group
})

export const questionTypeList = Object.values(menuItems)

export default menu
