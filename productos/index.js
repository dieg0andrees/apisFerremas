const express = require('express')
const oracledb = require('oracledb')

const app = express()
const port = 3000
const dbConfig = {
    user: 'entregaferramas',
    password:'entregaferramas',
    connectString:'localhost:1521/orcl'
}

app.use(express.json())

app.get('/', (req, res) => {
    res.status(200).json( {"mensaje": "Hola express 2"} )
})
//Aqui obtenemos todos los productos
app.get('/productos', async(req, res) =>{
    let cone
    try {
        cone = await oracledb.getConnection(dbConfig)
        const result = await cone.execute(
        `select 
            producto.id_producto,
            producto.NOMBRE_PRODUCTO,
            producto.PRECIO_PRODUCTO,
            producto.STOCK_PRODUCTO,
            MARCA.DESCRIPCION,
            tipo_producto.DESCRIPCION,
            producto.imagenes
        from producto
        join MARCA on producto.id_marca = MARCA.ID_MARCA
        join tipo_producto on producto.ID_TIPO_PRODUCTO = tipo_producto.id_tipo_producto`)
        res.json(result.rows.map(row =>({
            id_producto: row[0],
            nombre_producto: row[1],
            precio_producto: row[2],
            stock_producto: row[3],
            id_marca: row[4],
            id_tipo_producto: row[5],
            imagenes: row[6]
        })))
    } catch (ex) {
        res.status(500).json({error: ex.message})
    } finally {
        if (cone) await cone.close()
    }
})

app.get('/productos/:id_producto', async(req, res) =>{
    let cone
    const id_producto = parseInt(req.params.id_producto)
    try{
        cone = await oracledb.getConnection(dbConfig)
        const result = await cone.execute(
        `select 
            producto.id_producto,
            producto.NOMBRE_PRODUCTO,
            producto.PRECIO_PRODUCTO,
            producto.STOCK_PRODUCTO,
            MARCA.DESCRIPCION,
            tipo_producto.DESCRIPCION,
            producto.imagenes
        from producto
        join MARCA on producto.id_marca = MARCA.ID_MARCA
        join tipo_producto on producto.ID_TIPO_PRODUCTO = tipo_producto.id_tipo_producto
        where id_producto = :id_producto`, [id_producto])
        if (result.rows.length === 0){
            res.status(404).json({mensaje: "Producto no encontrado"})
        }else{
            const row = result.rows[0]
            res.json({
            id_producto: row[0],
            nombre_producto: row[1],
            precio_producto: row[2],
            stock_producto: row[3],
            id_marca: row[4],
            id_tipo_producto: row[5],
            imagenes: row[6]
            })
        }
    }catch (error){
        res.status(500).json({error: error.message})
    } finally {
        if (cone) cone.close()
    }
})

app.post('/productos', async (req, res) =>{
    let cone
    const {nombre_producto, precio_producto, stock_producto, id_marca, id_tipo_producto, imagenes} = req.body
    try{
        cone = await oracledb.getConnection(dbConfig)
        await cone.execute(
        `insert into producto(
        id_producto,
        nombre_producto,
        precio_producto,
        stock_producto,
        id_marca,
        id_tipo_producto,
        imagenes
        )
        values(
        seq_producto_id.nextval,
        :nombre_producto,
        :precio_producto,
        :stock_producto,
        :id_marca,
        :id_tipo_producto,
        :imagenes
        )`, {nombre_producto, precio_producto, stock_producto, id_marca, id_tipo_producto, imagenes},
        {autoCommit: true}
        )
        res.status(201).json({mensaje: "Producto creado"})
    }catch (error){
        res.status(500).json({error: error.message})
    } finally{
        if (cone) cone.close()
    }
})

app.put('/productos/:id_producto', async(req, res) =>{
    let cone
    const id_producto = parseInt(req.params.id_producto)
    const {nombre_producto, precio_producto, stock_producto, id_marca, id_tipo_producto, imagenes} = req.body
    try{
        cone = await oracledb.getConnection(dbConfig)
        const result = await cone.execute(`
            update producto
            set 
            nombre_producto = :nombre_producto,
            precio_producto = :precio_producto,
            stock_producto = :stock_producto,
            id_marca = :id_marca,
            id_tipo_producto = :id_tipo_producto,
            imagenes = :imagenes
            where id_producto = :id_producto
            `, {id_producto, nombre_producto, precio_producto, stock_producto, id_marca, id_tipo_producto, imagenes}, 
            {autoCommit: true}
        )
        if (result.rowsAffected===0){
            res.status(404).json({mensaje: "Producto no encontrado"})
        }else{
            res.json({mensaje: 'Producto modificado'})
        }
    }catch (error) {
        res.status(500).json({error: error.message})
    } finally {
        if (cone) cone.close()
    }
})

app.delete('/productos/:id_producto', async(req, res) =>{
    let cone
    const id_producto = parseInt(req.params.id_producto)
    try{
        cone = await oracledb.getConnection(dbConfig)
        const result = await cone.execute(
            `delete from producto
            where id_producto = :id_producto`,[id_producto], {autoCommit: true}
        )
        if(result.rowsAffected===0){
            res.status(404).json({mensjae: "Producto no encontrado"})
        }else{
            res.json({mensaje: "Producto eliminado"})
        }
    }catch (error) {
        res.status(500).json({error: error.message})
    }finally{
        if (cone) cone.close()
    }
})

app.patch('/productos/:id_producto', async(req, res) =>{
    let cone
    const id_producto = parseInt(req.params.id_producto)
    const {nombre_producto, precio_producto, stock_producto, id_marca, id_tipo_producto, imagenes} = req.body
    try{
        cone = await oracledb.getConnection(dbConfig)
        let campos = []
        let valores = {}
        if (nombre_producto !== undefined){
            campos.push('nombre_producto = :nombre_producto')
            valores.nombre_producto = nombre_producto
        }
        if (precio_producto !== undefined){
            campos.push('precio_producto = :precio_producto')
            valores.precio_producto = precio_producto
        }
        if (stock_producto !== undefined){
            campos.push('stock_producto = :stock_producto')
            valores.stock_producto = stock_producto
        }
        if (id_marca !== undefined){
            campos.push('id_marca = :id_marca')
            valores.id_marca = id_marca
        }
        if (id_tipo_producto !== undefined){
            campos.push('id_tipo_producto = :id_tipo_producto')
            valores.id_tipo_producto = id_tipo_producto
        }
        if (imagenes !== undefined){
            campos.push('imagenes = :imagenes')
            valores.imagenes = imagenes
        }

        if(campos.length===0){
            res.status(400).json({mensaje: 'No se enviaron campos para actulizar'})
        }
        valores.id_producto = id_producto

        const sql = `update producto set ${campos.join(', ')} where id_producto = :id_producto`
        const result = await cone.execute(
            sql, valores, {autoCommit:true}
        )
        if (result.rowsAffected===0){
            res.status(404).json({mensaje: "Producto no existe"})
        }else{
            res.json({mensje: "Producto actualizado parcialmente"})
        }
    }catch (error) {
        res.status(500).json({error: error.message})
    }finally{
        if (cone) cone.close()
    }
})



app.listen(port, () => {
    console.log(`API en puerto: ${port}`);
})