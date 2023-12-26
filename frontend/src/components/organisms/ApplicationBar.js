import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Drawer from '@mui/material/Drawer';
import APIKeySetting from '../molecules/APIKeySetting';

export default function ApplicationBar() {
  const [open, setOpen] = React.useState(false)

  function handleClick() {
    setOpen(true)
  }

  function toggleDrawer() {
    setOpen(false)
  }

  return (
    <AppBar position='static'>
      <Toolbar>
        <Typography variant='h3' sx={{ flexGrow: 1 }}>
          テレビ番組の要約ページを作成するツール
        </Typography>
        <Button color='inherit' size='large' onClick={handleClick}>
          <Typography>
            API鍵の設定
          </Typography>
        </Button>
        <Drawer
          anchor='right'
          open={open}
          onClose={toggleDrawer}
          PaperProps={{
            sx: { width: '750px' }
          }}
        >
          {['DeepL', 'OpenAI'].map(function(tool) {
            return (
              <div key={tool}>
                <APIKeySetting
                  tool={tool}
                />
              </div>
            )
          })}
        </Drawer>
      </Toolbar>
    </AppBar>
  )
}