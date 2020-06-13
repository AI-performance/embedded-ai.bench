// Tencent is pleased to support the open source community by making TNN available.
//
// Copyright (C) 2020 THL A29 Limited, a Tencent company. All rights reserved.
//
// Licensed under the BSD 3-Clause License (the "License"); you may not use this file except
// in compliance with the License. You may obtain a copy of the License at
//
// https://opensource.org/licenses/BSD-3-Clause
//
// Unless required by applicable law or agreed to in writing, software distributed
// under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
// CONDITIONS OF ANY KIND, either express or implied. See the License for the
// specific language governing permissions and limitations under the License.

#include "tnn/device/cpu/acc/cpu_reduce_layer_acc.h"
#include "tnn/utils/naive_compute.h"
#include "tnn/utils/data_type_utils.h"
#include "tnn/utils/dims_vector_utils.h"

namespace TNN_NS {

CpuReduceLayerAcc::~CpuReduceLayerAcc() {}

Status CpuReduceLayerAcc::Reshape(const std::vector<Blob *> &inputs, const std::vector<Blob *> &outputs) {
    return TNN_OK;
}

Status CpuReduceLayerAcc::Forward(const std::vector<Blob *> &inputs, const std::vector<Blob *> &outputs) {
    if (inputs.size() < 1) {
        LOGE("Error: invalid inputs count\n");
        return Status(TNNERR_LAYER_ERR, "layer's inputs size must >= 2");
    }
    auto layer_param = dynamic_cast<ReduceLayerParam *>(param_);
    if (!layer_param || layer_param->axis.size() != 1) {
        LOGE("Error: layer param is invalid\n");
        return Status(TNNERR_MODEL_ERR, "Error: layer param is invalid");
    }

    Blob *input_blob  = inputs[0];
    Blob *output_blob = outputs[0];
    auto input_dims   = input_blob->GetBlobDesc().dims;

    int axis = layer_param->axis[0];
    axis     = axis >= 0 ? axis : axis + (int)input_dims.size();
    if (axis < 0 || axis >= input_dims.size()) {
        LOGE("Error: layer param axis is invalid\n");
        return Status(TNNERR_MODEL_ERR, "Error: layer param axis is invalid");
    }

    int channels  = input_dims[axis];
    int outer_dim = DimsVectorUtils::Count(input_dims, 0, axis);
    int inner_dim = DimsVectorUtils::Count(input_dims, axis + 1);
    if (inner_dim == 0) {
        inner_dim = 1;
    }

    if (output_blob->GetBlobDesc().data_type == DATA_TYPE_FLOAT) {
        float *input_data  = static_cast<float *>(input_blob->GetHandle().base);
        float *output_data = static_cast<float *>(output_blob->GetHandle().base);

        int output_size = DimsVectorUtils::Count(output_blob->GetBlobDesc().dims);
        memset(output_data, 0, outer_dim * inner_dim * sizeof(float));

        CalculateReduce(output_data, input_data, outer_dim, channels, inner_dim);
    } else if (output_blob->GetBlobDesc().data_type == DATA_TYPE_INT8) {
        LOGE("Error: layer acc dont support datatype: %d\n", output_blob->GetBlobDesc().data_type);
        return Status(TNNERR_MODEL_ERR, "Error: layer acc dont support datatype");
    } else {
        LOGE("Error: layer acc dont support datatype: %d\n", output_blob->GetBlobDesc().data_type);
        return Status(TNNERR_MODEL_ERR, "Error: layer acc dont support datatype");
    }

    return TNN_OK;
}

}  // namespace TNN_NS
