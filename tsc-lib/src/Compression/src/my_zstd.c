/*
    AtriumDB is a timeseries database software designed to best handle the unique features and
    challenges that arise from clinical waveform data.
        Copyright (C) 2023  The Hospital for Sick Children

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <https:www.gnu.org/licenses/>.
*/

//
// Created by Will Dixon on 2021-05-12.
//
#include <my_compression.h>
#include <zstd.h>


size_t my_zstd_compress(unsigned char * data_in, unsigned char * compressed_out, size_t size_in,
                        size_t size_buf, int8_t compression_level){
    return ZSTD_compress(compressed_out, size_buf, data_in, size_in, compression_level);
}


size_t my_zstd_decompress(unsigned char *compressed_in, unsigned char *data_out, size_t size_in, size_t size_out)
{
    return ZSTD_decompress(data_out, size_out, compressed_in, size_in);
}

size_t get_zstd_compressBound(size_t size_in)
{
    return ZSTD_compressBound(size_in);
}
