# mcbe-admin
Admin tools for MCBE worlds

### Requirements

You will need python3 and a compiled dll or so of leveldb-mcpe (https://github.com/Mojang/leveldb-mcpe)

### Usage

python3 mcbe_admin.py [--lib <leveldb-mcpe-lib.so/dll>] [-r] [-p] [-c] [-w <worldBorderFile>] worldDirectory
 
#### Library
 Option : --lib <libraryFile>
 
 This is used to tell python where exactly is the compiled leveldb-mcpe lib

#### Mob removal
 Option : -r
 
 Remove mobs that are :
 - Not tagged
 - Not tamed
 - Not charged creepers
 - Natural spawns (not bred or from spawners)

#### Pending  tick tool
 Option : -p
 
 This removes duplicate pending ticks from chunks

#### World border tool
 Option : -w worldBorderFile

  The file is a CSV file that specifies which portions of the world you want to keep.
  
  Line format : "dimension,x,z,x1,z1"
  
  Or to keep an entire dimension : "dimension"
  
  Example :
  ```
  0,-4096,-4096,4096,4096
  1
  2
  ```
  This file specifies a world with the overworld limited to -4096 to 4096 in x and z coordonates, while keeping the nether and the end intact.
    
  Dimension can be :
  - 0 : overworld
  - 1 : nether
  - 2 : end

#### DB compactor
 Option : -c
 
 Make the program go over the db and tries to compact it. This is a feature from leveldb.

## Credits

This repository contains code from other repositories :
Mojang leveldb : https://github.com/Mojang/leveldb-mcpe
NBT : https://github.com/twoolie/NBT (works natively for java data, but needs to be modified for mcpe because of endianess)
Ctypes leveldb interface : https://github.com/jtolds/leveldb-py (slightly modified to match mojangs modification of leveldb)
