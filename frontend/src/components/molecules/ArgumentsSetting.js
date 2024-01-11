import React from 'react'
import TitleField from '../atoms/TitleField'
import NSummaryFiled from '../atoms/NSummaryField'

export default function ArgumentsSetting() {
  return (
    <div className='flex-col space-y-4'>
      <div>
        <TitleField />
      </div>
      <div>
        <NSummaryFiled />
      </div>
    </div>
  )
}