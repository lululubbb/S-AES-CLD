function showTab(tabId) {
    // 隐藏所有tab内容
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    // 显示对应tab内容
    document.getElementById(tabId).classList.add('active');
}

function showBit16Tab(action) {
    var encryptTab = document.getElementById('bit16-encrypt');
    var decryptTab = document.getElementById('bit16-decrypt');

    // 隐藏所有界面
    encryptTab.classList.remove('active');
    decryptTab.classList.remove('active');

    // 根据用户点击的按钮显示加密或解密
    if (action === 'encrypt') {
        encryptTab.classList.add('active'); // 显示加密界面
    } else if (action === 'decrypt') {
        decryptTab.classList.add('active'); // 显示解密界面
    }
}

// 显示 ASCII 加密或解密界面
function showASCIITab(action) {
    // 获取所有 ASCII 加密和解密的界面元素
    var encryptTab = document.getElementById('ascii-encrypt');
    var decryptTab = document.getElementById('ascii-decrypt');
    
    // 隐藏所有界面
    encryptTab.classList.remove('active');
    decryptTab.classList.remove('active');
    
    // 根据用户点击的按钮显示加密或解密
    if (action === 'encrypt') {
        encryptTab.classList.add('active'); // 显示加密界面
    } else if (action === 'decrypt') {
        decryptTab.classList.add('active'); // 显示解密界面
    }
}

// 显示文件加密或解密界面
function showFileTab(action) {
    // 获取所有文件加密和解密的界面元素
    var encryptTab = document.getElementById('file-encrypt');
    var decryptTab = document.getElementById('file-decrypt');
    
    // 隐藏所有界面
    encryptTab.classList.remove('active');
    decryptTab.classList.remove('active');
    
    // 根据用户点击的按钮显示加密或解密
    if (action === 'encrypt') {
        encryptTab.classList.add('active'); // 显示加密界面
    } else if (action === 'decrypt') {
        decryptTab.classList.add('active'); // 显示解密界面
    }
}

//重置
function resetInputs() {
    document.querySelectorAll('input').forEach(input => input.value = '');
    document.getElementById("bit8-plaintext").value = "";
    document.getElementById("bit8-key").value = "";
    document.getElementById("bit8-ciphertext").innerText = "";
    document.getElementById("bit8-key-decrypt").innerText = "";
}

// 重置输入
function resetASCIIInputs() {
    document.getElementById("ascii-plaintext").value = "";
    document.getElementById("ascii-ciphertext").value = "";
    document.getElementById("ascii-result-encrypt").innerText = "";
    document.getElementById("ascii-result-decrypt").innerText = "";
}

// 重置文件输入
function resetFileInputs() {
    document.getElementById("file-input-encrypt").value = "";
    document.getElementById("file-input-decrypt").value = "";
    document.getElementById("file-result-encrypt").innerText = "";
    document.getElementById("file-result-decrypt").innerText = "";
}

//选择文件按钮
document.getElementById('custom-file-input-encrypt').addEventListener('click', function() {
    document.getElementById('file-input-encrypt').click();
});

document.getElementById('custom-file-input-decrypt').addEventListener('click', function() {
    document.getElementById('file-input-decrypt').click();
});



// 发送加密请求到后端
async function encrypt16Bit() {
    const plaintext = document.getElementById('bit16-plaintext').value;
    const key = document.getElementById('bit16-key').value;
    const encryptionType = document.querySelector('input[name="encryptionType"]:checked').value;

    let url = 'http://127.0.0.1:8050/encrypt16Bit';
    if (encryptionType === 'SAES') {
        url = 'http://127.0.0.1:8050/encrypt16Bit';
    } else if (encryptionType === '2AES') {
        url = 'http://127.0.0.1:8050/encrypt16Bit_2AES';
    } else if (encryptionType === '3AES') {
        url = 'http://127.0.0.1:8050/encrypt16Bit_3AES';
    }

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            key: key,
            plaintext: plaintext,
        }),
    });

    const data = await response.json();
    document.getElementById('bit16-result').innerText = `加密后的密文是：${data.encrypted}`;
}

// 发送解密请求到后端
async function decrypt16Bit() {
    const ciphertext = document.getElementById('bit16-ciphertext').value;
    const key = document.getElementById('bit16-key-decrypt').value;
    const decryptionType = document.querySelector('input[name="decryptionType"]:checked').value;

    let url = 'http://127.0.0.1:8050/decrypt16Bit';
    if (decryptionType === 'SAES') {
        url = 'http://127.0.0.1:8050/decrypt16Bit';
    } else if (decryptionType === '2AES') {
        url = 'http://127.0.0.1:8050/decrypt16Bit_2AES';
    } else if (decryptionType === '3AES') {
        url = 'http://127.0.0.1:8050/decrypt16Bit_3AES';
    }

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            key: key,
            ciphertext: ciphertext,
        }),
    });

    const data = await response.json();
    document.getElementById('bit16-result-decrypt').innerText = `解密后的明文是：${data.decrypted}`;
}

// ASCII 加密
async function encryptASCII() {
    const plaintext = document.getElementById('ascii-plaintext').value;
    const key = document.getElementById("ascii-key").value;
    const mode = document.querySelector('input[name="encryptionMode"]:checked').value; // 获取加密模式
    let url;

    // 根据选定的模式设置不同的URL
    if (mode === 'Normal') {
        url = 'http://localhost:8050/encrypt_ascii';
    } else if (mode === 'CBC') {
        url = 'http://localhost:8050/encrypt_ascii_CBC';
    }

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ plaintext: plaintext, key: key }),
    });
    
    const data = await response.json();
    console.log(data);
    document.getElementById('ascii-result-encrypt').innerText = `加密结果：${data.encrypted}`;
}

// ASCII 解密
async function decryptASCII() {
    const ciphertext = document.getElementById('ascii-ciphertext').value;
    const key = document.getElementById("ascii-key-decrypt").value;
    const mode = document.querySelector('input[name="decryptionMode"]:checked').value; // 获取解密模式
    let url;

    // 根据选定的模式设置不同的URL
    if (mode === 'Normal') {
        url = 'http://localhost:8050/decrypt_ascii';
    } else if (mode === 'CBC') {
        url = 'http://localhost:8050/decrypt_ascii_CBC';
    }

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ciphertext: ciphertext, key: key }),
    });
    
    const data = await response.json();
    console.log(data);
    document.getElementById('ascii-result-decrypt').innerText = `解密结果：${data.decrypted}`;
}


// 文件加密
async function encryptFile() {
    const fileInput = document.getElementById('file-input-encrypt');
    const key = document.getElementById("file-key").value;
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('key',key);
    const response = await fetch('http://localhost:8050/encrypt_file', {
        method: 'POST',
        body: formData,
    });

    const data = await response.json();
    console.log(data)
    document.getElementById('file-result-encrypt').innerText = `加密结果：${data.encrypted}`;
}

// 文件解密
async function decryptFile() {
    const fileInput = document.getElementById('file-input-decrypt');
    const key = document.getElementById("file-key-decrypt").value;
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('key',key);
    const response = await fetch('http://localhost:8050/decrypt_file', {
        method: 'POST',
        body: formData,
    });

    const data = await response.json();
    console.log(data)
    document.getElementById('file-result-decrypt').innerText = `解密结果：${data.decrypted}`;
}

// 中间相遇
async function attack() {
    const plaintext = document.getElementById('violent-plaintext').value;
    const ciphertext = document.getElementById("violent-ciphertext").value;
    const response = await fetch('http://localhost:8050/attack', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            plaintext: plaintext, 
            ciphertext: ciphertext, 
        }),
    });

    const data = await response.json();
    console.log(data)
 if (Array.isArray(data.key) && data.key.length > 0) {
    const keysStrings = data.key.map(k => `[${k.join(',')}]`).join('<br>'); 
    document.getElementById('violent-result-encrypt').innerHTML = `找到的密钥：<br>${keysStrings}<br>`;
} else {
    document.getElementById('violent-result-encrypt').innerText = "未找到密钥";
}
}


// 更新结果提示文本
function updateResultText(mode) {
    let encryptionType = document.querySelector('input[name="encryptionType"]:checked')?.value || '3AES';
    let decryptionType = document.querySelector('input[name="decryptionType"]:checked')?.value || '3AES';
    let resultEncrypt = document.getElementById('bit16-result');
    let resultDecrypt = document.getElementById('bit16-result-decrypt');
    
    if (mode === 'encrypt') {
        resultEncrypt.textContent = '此处显示' + encryptionType + '加密结果';
    } else if (mode === 'decrypt') {
        resultDecrypt.textContent = '此处显示' + decryptionType + '解密结果';
    }
}


// 初始化时调用以更新默认显示的文本
updateResultText('encrypt');
updateResultText('decrypt');

function updateKeyInput(mode) {
    let keyLabel = mode === 'encrypt' ? document.getElementById('encrypt-key-label') : document.getElementById('decrypt-key-label');
    let keyInput = mode === 'encrypt' ? document.getElementById('bit16-key') : document.getElementById('bit16-key-decrypt');

    // 判断选择的加密类型
    if (mode === 'encrypt') {
        if (document.getElementById('saes').checked) {
            keyLabel.textContent = "请输入16位二进制密钥";
            keyInput.maxLength = 16;
            keyInput.placeholder = "如: 0110110100101101";
        } else {
            keyLabel.textContent = "请输入32位二进制密钥";
            keyInput.maxLength = 32;
            keyInput.placeholder = "如: 01101101001011010110110100101101";
        }
    } else {
        // 解密部分的密钥输入更新
        if (document.getElementById('saes-decrypt').checked) {
            keyLabel.textContent = "请输入16位二进制密钥";
            keyInput.maxLength = 16;
            keyInput.placeholder = "如: 0110110100101101";
            keyInput.oninput="this.value = this.value.replace(/[^01]/g, '');"
        } else {
            keyLabel.textContent = "请输入32位二进制密钥";
            keyInput.maxLength = 32;
            keyInput.placeholder = "如: 01101101001011010110110100101101";
        }
    }
}



// 更新密钥输入框时调用
document.querySelectorAll('input[name="encryptionType"]').forEach((elem) => {
    elem.addEventListener('change', () => {
        updateKeyInput('encrypt');
        updateResultText('encrypt'); // 也更新加密结果文本
    });
});
document.querySelectorAll('input[name="decryptionType"]').forEach((elem) => {
    elem.addEventListener('change', () => {
        updateKeyInput('decrypt');
        updateResultText('decrypt'); // 也更新解密结果文本
    });
});


// 更新ASCII结果提示文本
function updateASCIIResultText(mode) {
    let encryptionMode = document.querySelector('input[name="encryptionMode"]:checked')?.value || 'Normal';
    let decryptionMode = document.querySelector('input[name="decryptionMode"]:checked')?.value || 'Normal';
    let resultEncrypt = document.getElementById('ascii-result-encrypt');
    let resultDecrypt = document.getElementById('ascii-result-decrypt');
    
    if (mode === 'encrypt') {
        resultEncrypt.textContent = '此处显示' + encryptionMode + '加密结果';
    } else if (mode === 'decrypt') {
        resultDecrypt.textContent = '此处显示' + decryptionMode + '解密结果';
    }
}

// 初始化时调用以更新默认显示的文本
updateASCIIResultText('encrypt');
updateASCIIResultText('decrypt');

